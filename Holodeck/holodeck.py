from string import capitalize
import threading
from effects import get_all_effects
from pipe import Pipe
import time

def id_to_classname(cmd):
  return "%sEffect" % (capitalize(cmd))

def classname_to_id(key):
  return key[:-6].lower()

class Holodeck(threading.Thread):
  
  def __init__(self, effect_list, update_func):
    threading.Thread.__init__(self)
    self.update_func = update_func

    self.state = {
      'env': None, 
      'mod': None,
      'time': None,
      'battle': None
    }

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
    for pipe in Pipe.items():
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
    while True:
      self.update()
      time.sleep(0.5)

  def update(self):
    # Compose controllers into single environment
    env = self.compose()
    
    # Use a separate function to complete updates
    self.update_func(env)

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
      print "Looking for key", req
      if turn_on:
        state_delta[classname_to_id(req)] = True
        if req in self.activeEffects:
          raise Exception("Effect already in effect")
        
        # Create a new effect with this request.
        # This may affect other active effects
        eff = self.effectClasses[req](self.activeEffects, self.pipelines)
        eff.register()
      else:
        state_delta[classname_to_id(req)] = False
        self.activeEffects[req].request_exit()

    # Write back the change in state
    return state_delta

def create_deck():
  from serial import Serial
  from Tests.TestSerial import TestSerial
  from Outputs.RelayController import RelayController
  from Outputs.RGBSingleController import RGBSingleController
  from Outputs.RGBMultiController import RGBMultiController, RGBState
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

  last_img_wall = None
  last_img_window = None
  def update_room(env):
    # Update the room to match the environment
    if env[Pipe.WINDOWTOP] and env[Pipe.WINDOWBOT]:
      window.write(
        env[Pipe.WINDOWTOP],
        env[Pipe.WINDOWBOT],
      )
    else:
      window.write(
        [0,0,0],
        [0,0,0]
      )

    if env[Pipe.FLOOR]:
      couch.write(env[Pipe.FLOOR])
    else:
      couch.write([0,0,0])

    if env[Pipe.TOWER] and env[Pipe.RING]:
      for (i,c) in enumerate(env[Pipe.TOWER]+env[Pipe.RING]):
        tower.manual_write(i, c)
      tower.manual_update()
    else:
      for i in xrange(105+24):
        tower.manual_write(i, [0,0,0])
      tower.manual_update()

    proj_window.zoom_to(env[Pipe.WINDOWIMG])
    proj_wall.slide_to(env[Pipe.WALLIMG])

    #controls['IR_AC'].setState(env['temp'])

    if env[Pipe.LIGHTS]:
      lights.set_state(env[Pipe.LIGHTS])
    else:
      lights.set_state(False)
    
  # Start up the holodeck
  deck = Holodeck(get_all_effects(), update_room)
  return deck

if __name__ == "__main__":
  deck = create_deck()
  # Test to see what the deck does
  print deck.handle({'paul': True})
  deck.update()

