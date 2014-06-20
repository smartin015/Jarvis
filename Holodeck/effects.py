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

  def __init__(self, active_effects, pipes):
    self.should_exit = False
    self.pipes = pipes
    self.active_effects = active_effects

  def get_blacklist(self):
    """ Return a list of typenames that this effect 
        should not run alongside
    """
    return []

  def register(self):
    """ Effect injects itself into its own location(s) 
        in the controller pipeline
    """
    # TODO: blacklist booting

    # Remove from pipeline
    for (pipe_id, con) in self.get_mapping().items():
      self.pipes[pipe_id].append(con)
      self.pipes[pipe_id].sort(key=lambda con:con[1])

    # Add to active effects
    self.active_effects[self.__class__.__name__] = self


  def get_mapping(self):
    raise Exception("Unimplemented")

  def remove(self):
    """ Removes ourselves from the pipeline """
    # TODO: Mutex this!
    for (pipe_id, con) in self.get_mapping().items():
      try:
        idx = self.pipes[pipe_id].index(con)
        del self.pipes[pipe_id][idx]
      except ValueError:
        print self.pipes
        raise

    # Remove from active effects
    del self.active_effects[self.__class__.__name__]

  def request_exit(self):
    """ Tell this effect to start the process of dying 
    """
    self.should_exit = True

  def post_render(self):
    """ Called once per frame for update purposes. 
        Remember to check self.should_exit() here
    """
    if self.should_exit:
      self.remove()



class ForestEffect(EffectTemplate):
  META = {
    'tab': "locations",
    'text': "Forest",
  }

  def get_mapping(self):
    return {
      P.FLOOR: (self.floor, 1),
      P.WINDOWTOP: (self.window_top, 1),
      P.WINDOWBOT: (self.window_bot, 1),
    }

  def floor(self, prev):
    return [55, 155, 55]

  def window_top(self, prev):
    return [255, 0, 0]

  def window_bot(self, prev):
    return [100, 50, 20]


class RainEffect(EffectTemplate):
  META = {
    'tab': "atmosphere",
    'text': "Rain",
  }

  def get_mapping(self):
    return {
      P.TOWER: (self.tower, 1),
      P.RING: (self.ring, 1),
    }

  def tower(self, prev):
    return [[0, 0, 255]]*NLIGHTS

  def ring(self, prev):
    return [[128, 128, 255]]*NRING


class BattleEffect(EffectTemplate):
  META = {
    'tab': "effects",
    'text': "Battle",
  }

  def get_mapping(self):
    return {
      P.WINDOWTOP: (self.window_top, 1),
      P.WINDOWBOT: (self.window_bot, 1)
    }

  def window_top(self, prev):
    return [255, 0, 0]

  def window_bot(self, prev):
    return [255, 0, 0]


class DayEffect(EffectTemplate):
  META = {
    'tab': "atmosphere",
    'text': "Daytime",
  }

  def get_mapping(self):
    return {
      P.LIGHTS: (self.lights, 1)
    }

  def lights(self, prev):
    return True

class PaulEffect(EffectTemplate):
  META = {
    'tab': "effects",
    'text': "Paul-ify",
  }

  def get_mapping(self):
    return {
      P.FLOOR: (self.floor, 1),
      P.WINDOWTOP: (self.window_top, 1),
      P.WINDOWBOT: (self.window_bot, 1),
    }

  def floor(self, prev):
    return [80, 180, 0]

  def window_top(self, prev):
    return [20, 100, 255]
    #sky blue: return [20, 100, 255]
	#plains grass: return [80, 180, 0] 
	#sandish: return [180, 140, 100]

  def window_bot(self, prev):
    return [100, 50, 20]



