from string import capitalize
from SortedCollection import SortedCollection

class Pipe():
  RING = "towerRing"
  TOWER = "tower"
  LIGHTS = "lights"
  WINDOWIMG = "windowimg"
  WALLIMG = "wallimg"
  FLOOR = "floor"
  WINDOWTOP = "windowtop"
  WINDOWBOT = "windowbot"
  TEMP = "temp"
  SOUND = "sound"

  @classmethod
  def items(self):
    return [a for a in self.__dict__.values() if type(a) is str and not a.startswith("__")]

class Holodeck():
  
  def __init__(self, effect_list, update_func):
    self.update_func = update_func

    self.state = {
      'env': None, 
      'mod': None,
      'time': None,
      'battle': None
    }

    # Create a dictionary of effects keyed by class name
    self.effectClasses = {}
    for cls in effect_list:
      self.effectClasses[cls.__name__] = cls

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
      self.pipelines[pipe] = SortedCollection()

  def _cmd_to_key(self, cmd):
    return "%sEffect" % (capitalize(cmd))

  def compose(self):
    # Composes each controller pipeline into a single environment
    env = dict()
    for name in self.pipelines:
      composite = None
      for (con, priority) in self.pipelines[name]:
        composite = con(composite)
      env[name] = composite
    return env

  def update(self):
    # Compose controllers into single environment
    env = self.compose()
    
    # Use a separate function to complete updates
    self.update_func(env)

    # Finally, give the effect objects a chance to adjust themselves
    # (usually, to remove themselves from )
    for (name, effect) in self.activeEffects.items():
      effect.post_render(self)

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
      req = self._cmd_to_key(req)
      if turn_on:
        state_delta[req] = True
        if req in self.activeEffects:
          raise Exception("Effect already in effect")
        
        # Create a new effect with this request
        self.activeEffects[req] = self.effectClasses[req]()
        blacklist = self.activeEffects[req].get_blacklist()

        # Tell conflicting effects to end
        for badclass in blacklist:
          badeffect = self.activeEffects.get(badclass.__name__, None)
          badeffect.request_exit()
          state_delta[badclass.__name__] = False

        # Inject the new effect into the pipeline
        self.activeEffects[req].inject_into(self.pipelines)
      else:
        self.activeEffects[req].request_exit()

    # Write back the change in state
    return state_delta




if __name__ == "__main__":
  from serial import Serial
  from Tests.TestSerial import TestSerial
  from Outputs.RelayController import RelayController
  from Outputs.RGBSingleController import RGBSingleController
  from Outputs.RGBMultiController import RGBMultiController, RGBState
  from Outputs.IRController import IRController
  from effects import *
  import time

  # TODO: Use getmembers?
  effect_list = [
    ForestEffect,
    RainEffect,
    BattleEffect,
    DayEffect,
    # TODO: All effects
  ]

  window = RGBSingleController(Serial("/dev/ttyUSB1", 9600))
  couch = RGBSingleController(Serial("/dev/ttyUSB0", 9600))
  tower = RGBMultiController(Serial("/dev/ttyACM0", 115200))
    #"IR_AC": IRController(TestSerial("AC")),
  lights = RelayController(Serial("/dev/ttyUSB2", 9600))
  time.sleep(2.5) # Need delay at least this long for arduino to startup

  tower.setState(RGBState.STATE_MANUAL)
  time.sleep(1.0)

  def update_room(env):
    #for (k,v) in env.items():
    #  print k, v
    # Update the room to match the environment
    window.write(
      env[Pipe.WINDOWTOP],
      env[Pipe.WINDOWBOT],
    )
    couch.write(env[Pipe.FLOOR])
    
    if env[Pipe.TOWER] and env[Pipe.RING]:
      for (i,c) in enumerate(env[Pipe.TOWER]+env[Pipe.RING]):
        tower.manual_write(i, c)
      tower.manual_update()
    #controls['IR_AC'].setState(env['temp'])
    lights.set_state(env[Pipe.LIGHTS])
    # TODO: Video screens

  # Start up the holdeck
  deck = Holodeck(effect_list, update_room)

  # Test to see what the deck does
  print deck.handle({'day': True, 'rain': True, 'forest': True})
  deck.update()

  time.sleep(3.0)