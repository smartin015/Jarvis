from pipe import Pipe as P
from Outputs.RGBMultiController import NLIGHTS, NRING

def get_all_effects():
  import inspect
  import sys
  effect_list = inspect.getmembers(sys.modules[__name__], inspect.isclass)
  return dict([(k,v) for k,v in effect_list if k.endswith('Effect')])

class EffectTemplate():
  META = {
    'tab': None,
    'id': None,
    'text': None,
    'img': None,
  }

  def get_blacklist(self):
    """ Return a list of typenames that this effect 
        should not run alongside
    """
    return []

  def inject_into(self, pipes):
    """ Effect injects itself into its own location(s) 
        in the controller pipeline
    """

    raise Exception("Unimplemented")

  def request_exit(self):
    """ Tell this effect to start the process of dying 
    """

  def post_render(self, holodeck):
    """ Called once per frame for update purposes. """
    pass


class ForestEffect(EffectTemplate):
  META = {
    'tab': "tab1",
    'id': "forest",
    'text': "Forest",
    'img': "forest.png",
  }
  def __init__(self):
    self.counter = 0

  def inject_into(self, pipes):
    pipes[P.FLOOR].insert((self.floor, 1))
    pipes[P.WINDOWTOP].insert((self.window_top, 1))
    pipes[P.WINDOWBOT].insert((self.window_bot, 1))

  def floor(self, prev):
    return [55, 155, 55]

  def window_top(self, prev):
    return [255, 0, 0]

  def window_bot(self, prev):
    return [100, 50, 20]

  def post_render(self, holodeck):
    self.counter += 1

class RainEffect(EffectTemplate):
  META = {
    'tab': "tab1",
    'id': "rain",
    'text': "Rain",
    'img': "rain.png",
  }
  def inject_into(self, pipes):
    pipes[P.TOWER].insert((self.tower, 1))
    pipes[P.RING].insert((self.ring, 1))

  def tower(self, prev):
    return [[0, 0, 255]]*NLIGHTS

  def ring(self, prev):
    return [[128, 128, 255]]*NRING


class BattleEffect(EffectTemplate):
  META = {
    'tab': "tab1",
    'id': "battle",
    'text': "Battle",
    'img': "cave.png",
  }
  def inject_into(self, pipes):
    pass


class DayEffect(EffectTemplate):
  META = {
    'tab': "tab1",
    'id': "day",
    'text': "Daytime",
    'img': "plains.png",
  }
  def inject_into(self, pipes):
    pipes[P.LIGHTS].insert((self.lights, 1))

  def lights(self, prev):
    return True

class PaulEffect(EffectTemplate):
  META = {
    'tab': "tab1",
    'id': "paul",
    'text': "Paul-ify",
    'img': "beach.png",
  }
  def inject_into(self, pipes):
    pipes[P.FLOOR].insert((self.floor, 1))
    pipes[P.WINDOWTOP].insert((self.window_top, 1))
    pipes[P.WINDOWBOT].insert((self.window_bot, 1))

  def floor(self, prev):
    return [80, 180, 0]

  def window_top(self, prev):
    return [20, 100, 255]
    #sky blue: return [20, 100, 255]
	#plains grass: return [80, 180, 0] 
	#sandish: return [180, 140, 100]

  def window_bot(self, prev):
    return [100, 50, 20]



