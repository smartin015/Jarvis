from string import capitalize
import threading
from effects import get_all_effects
from pipe import Pipe as P
import time
import logging
from pygame.time import Clock

def id_to_classname(cmd):
  return "%sEffect" % (capitalize(cmd))

def classname_to_id(key):
  return key[:-6].lower()

class Holodeck(threading.Thread):
  
  def __init__(self, effect_list, update_funcs):
    self.logger = logging.getLogger('Holodeck')
        
    threading.Thread.__init__(self)
    self.update_funcs = update_funcs

    # Create a dictionary of effects keyed by class name
    self.effectClasses = effect_list

    # When effects are instantiated, they are listed here.
    # New effects can request existing effects to go away,
    # Which allows for fading in/out.
    self.activeEffects = dict()

    # Each array represents a pipeline of control functions, linked
    # from effect objects.
    # Subsequent functions are passed in the previous functions' outputs.
    # Composition is left-to-right
    self.pipelines = {}
    for pipe in P.items():
      self.pipelines[pipe] = []

  def is_active(self, cmd):
    return (id_to_classname(cmd) in self.activeEffects)

  def compose(self):
    # Composes each controller pipeline into a single environment
    env = dict()
    for name in self.pipelines:
      composite = None
      for (con, priority) in self.pipelines[name]:
        composite = con(composite)
      env[name] = composite
    return env

  def run(self):
    c = Clock()
    while True:
      self.update()
      c.tick(10)

  def update(self):
    # Compose controllers into single environment
    env = self.compose()
    
    # Use a separate function to complete updates
    # TODO: Multi-thread pipeline and updates
    for (deps, func) in self.update_funcs:
      func(*[env[pipe_id] for pipe_id in deps if env[pipe_id] is not None])

    # Finally, give the effect objects a chance to adjust themselves
    # (usually, to remove themselves from )
    for (name, effect) in self.activeEffects.items():
      effect.post_render()

  def handle(self, request):
    # Request is in JSON format,
    # Specifying any of the following keys with a boolean true/false to update:
    #    - cave, town, river, ocean (environment effects)
    #    - rain, snow, campfire (modifiers)
    #    - day, night (times. transitions w/ sunrise & sunset)
    #    - battle (big, flashy, for beginning of fights)
    #
    # See self.effectClasses for a full list

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
        eff = self.effectClasses[req](self.activeEffects, self.pipelines)
        eff.register()
      else:
        self.logger.info("Removing " + req)
        state_delta[classname_to_id(req)] = False
        self.activeEffects[req].request_exit()

    # Write back the change in state
    return state_delta

def create_deck():
  from serial import Serial
  from Tests.TestSerial import TestSerial
  from Outputs.RelayController import RelayController
  from Outputs.RGBSingleController import RGBSingleController
  from Outputs.RGBMultiController import RGBMultiController, RGBState, NTOWER, NRING
  from Outputs.IRController import IRController
  from Outputs.ScreenController import ScreenController
  import socket

  window = RGBSingleController(Serial("/dev/ttyUSB1", 9600))
  couch = RGBSingleController(Serial("/dev/ttyUSB0", 9600))
  tower = RGBMultiController(Serial("/dev/ttyACM0", 115200))
  proj_window = ScreenController("192.168.1.100")
  proj_wall = ScreenController("192.168.1.23", imgpath="Assets/Images/")
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
    
  # Start up the holodeck
  deck = Holodeck(
    get_all_effects(), 
    [
      ([P.WINDOWTOP, P.WINDOWBOT], update_window_leds),
      ([P.FLOOR], update_floor_leds),
      ([P.TOWER, P.RING], update_tower_ring),
      ([P.WINDOWIMG], update_window_img),
      ([P.WALLIMG], update_wall_img),
      ([P.LIGHTS], update_lights),
    ]
  )
  return deck

if __name__ == "__main__":
  deck = create_deck()
  # Test to see what the deck does
  print deck.handle({'paul': True})
  deck.update()

