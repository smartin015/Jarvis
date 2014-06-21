from string import capitalize
import threading
from effects import get_all_effects
from effect_template import id_to_classname, classname_to_id
from pipe import Pipe as P
import time
import logging
from pygame.time import Clock

class Holodeck(threading.Thread):
  
  def __init__(self, effect_list, pipelines, update_funcs, state_callback=None):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.setLevel(logging.DEBUG)
        
    threading.Thread.__init__(self)
    self.update_funcs = update_funcs

    # Create a dictionary of effects keyed by class name
    self.effectClasses = effect_list

    self.state_callback = state_callback

    # When effects are instantiated, they are listed here.
    # New effects can request existing effects to go away,
    # Which allows for fading in/out.
    self.activeEffects = dict()

    # Each array represents a pipeline of control functions, linked
    # from effect objects.
    # Subsequent functions are passed in the previous functions' outputs.
    # Composition is left-to-right
    self.pipelines = {}
    self.initial_pipe_values = {}
    for pipe in pipelines:
      self.pipelines[pipe] = []
      self.initial_pipe_values[pipe] = pipelines[pipe]

  def is_active(self, cmd):
    return (id_to_classname(cmd) in self.activeEffects)

  def compose(self):
    # Composes each controller pipeline into a single environment
    env = dict()
    for name in self.pipelines:
      composite = self.initial_pipe_values[name]
      for (con, priority) in self.pipelines[name]:
        composite = con(composite)
      env[name] = composite
    return env

  def run(self):
    c = Clock()
    self.logger.debug("Beginning main loop")
    while True:
      self.update()
      c.tick(30)

  def update(self):
    # Compose controllers into single environment
    env = self.compose()
    # Use a separate function to complete updates
    # TODO: Multi-thread pipeline and updates
    for (deps, func) in self.update_funcs:
      pipes = [env[pipe_id] for pipe_id in deps]
      func(*pipes)

    # Finally, give the effect objects a chance to adjust themselves
    # (usually, to remove themselves from )
    for (name, effect) in self.activeEffects.items():
      effect.post_render()

  def handle_effect_exit(self, effect):
    state = {classname_to_id(effect.__class__.__name__): False}
    self.state_callback(state)

  def handle(self, request):
    # Request is in JSON format,
    # Specifying any of the following keys with a boolean true/false to update:
    #    - cave, town, river, ocean (environment effects)
    #    - rain, snow, campfire (modifiers)
    #    - day, night (times. transitions w/ sunrise & sunset)
    #    - battle (big, flashy, for beginning of fights)
    #
    # See self.effectClasses for a full list
    self.logger.debug("Got request %s" % str(request))
    state_delta = {}
    for (req, turn_on) in request.items():
      req = id_to_classname(req)
      if turn_on:
        self.logger.info("Adding " + req)
        state_delta[classname_to_id(req)] = True
        if req in self.activeEffects:
          raise Exception("Effect already in effect")
        
        # Create a new effect with this request.
        # This may affect other active effects
        eff = self.effectClasses[req](self.pipelines, self.activeEffects, self.handle_effect_exit)

        self.logger.info("Registering")
        eff.register()
      elif self.activeEffects.get(req):
        self.logger.info("Removing " + req)
        state_delta[classname_to_id(req)] = False
        self.activeEffects[req].request_exit()

    # Write back the change in state to ALL clients
    self.logger.debug("Handing off to callback")
    self.state_callback(state_delta)


last_sound = []
def create_deck():
  from serial import Serial
  from Tests.TestSerial import TestSerial
  from Outputs.RelayController import RelayController
  from Outputs.RGBSingleController import RGBSingleController
  from Outputs.RGBMultiController import RGBMultiController, RGBState, NTOWER, NRING
  from Outputs.IRController import IRController
  from Outputs.ScreenController import ScreenController
  from Outputs.AudioController import AudioController
  import socket

  window = RGBSingleController(Serial("/dev/ttyUSB1", 9600))
  couch = RGBSingleController(Serial("/dev/ttyUSB0", 9600))
  tower = RGBMultiController(Serial("/dev/ttyACM0", 115200))
  proj_window = ScreenController("192.168.1.100")
  proj_wall = ScreenController("192.168.1.23", imgpath="Assets/Images/")
  audio = AudioController("192.168.1.100")
  #"IR_AC": IRController(TestSerial("AC")),
  lights = RelayController(Serial("/dev/ttyUSB2", 9600))
  time.sleep(2.5) # Need delay at least this long for arduino to startup

  tower.setState(RGBState.STATE_MANUAL)
  time.sleep(1.0)

  tower_default = [[0,0,0]]*NTOWER
  ring_default = [[0,0,0]]*NRING
  black = [0,0,0]

  def update_window_leds(top=black, bot=black):
    window.write(top, bot)  

  def update_floor_leds(rgb=black):
    couch.write(rgb)
  
  def update_tower_ring(trgb=tower_default, rrgb=ring_default):
    for (i,c) in enumerate(trgb+rrgb):
      tower.manual_write(i, c)
    tower.manual_update()

  def update_window_img(img=None):
    proj_window.zoom_to(img)
  
  def update_wall_img(img=None):
    proj_wall.slide_to(img)

  def update_lights(is_on=False):
    lights.set_state(is_on)

  
  def update_sound(sounds=[]):
    global last_sound
    for s in sounds:
      if s not in last_sound:
        audio.play(s)
    for s in last_sound:
      if s not in sounds:
        audio.fade_out(s)
    last_sound = sounds
      
  # Start up the holodeck
  deck = Holodeck(
    get_all_effects(), 
    {
      P.WINDOWTOP: None,
      P.WINDOWBOT: None,
      P.FLOOR: None,
      P.TOWER: None,
      P.RING: None,
      P.WINDOWIMG: None,
      P.WALLIMG: None,
      P.LIGHTS: None,
      P.SOUND: None, 
      P.TEMP: None,
    },
    [
      ([P.WINDOWTOP, P.WINDOWBOT], update_window_leds),
      ([P.FLOOR], update_floor_leds),
      ([P.TOWER, P.RING], update_tower_ring),
      ([P.WINDOWIMG], update_window_img),
      ([P.WALLIMG], update_wall_img),
      ([P.LIGHTS], update_lights),
      ([P.SOUND], update_sound),
    ]
  )
  return deck

if __name__ == "__main__":
  deck = create_deck()
  # Test to see what the deck does
  print deck.handle({'fire': True})
  deck.run()

