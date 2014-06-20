from pipe import Pipe as P
from Outputs.RGBMultiController import NTOWER, NRING
from Holodeck.effect_template import EffectTemplate

def get_all_effects():
  import inspect
  import sys
  effect_list = inspect.getmembers(sys.modules[__name__], inspect.isclass)
  return dict([(k,v) for k,v in effect_list if k.endswith('Effect')])

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
    return [[0, 0, 255]]*NTOWER

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



