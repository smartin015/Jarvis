from pipe import Pipe as P
from Outputs.RGBMultiController import NTOWER, NRING
from Holodeck.effect_template import EffectTemplate
from random import randint

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

  def setup(self):
    self.count = 0
    self.arrcount = 0
    self.towerRGB = [[0, 0, 0]]*NTOWER

  def get_mapping(self): 
    return {
      P.TOWER: (self.tower, 1),
      P.RING: (self.ring, 1),
    }

  def tower(self, prev):
    print self.arrcount
    
    if self.towerRGB[self.arrcount][2] > 1:
    	self.towerRGB[self.arrcount][2] = (self.towerRGB[self.arrcount][2] - 5)
    else:
      self.towerRGB[self.arrcount][2] = 150

    self.arrcount = (self.arrcount + 1)
    if self.arrcount >= NTOWER:
      self.arrcount = 0;

    return self.towerRGB

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

class FireEffect(EffectTemplate):
  META = {
    'tab': "effects",
    'text': "Fire",
  }

  def get_mapping(self):
    return {
      P.FLOOR: (self.floor, 1),
    } 

  RED_MAX = 150
  GREEN_MAX = 40

  RED_MIN = 120
  GREEN_MIN = 10

  def setup(self):
    self.red = 170
    self.green = 20

  def floor(self, prev):
    if randint(0,1) == 1:
      if self.red < (self.RED_MAX - 5):
        self.red = (self.red + 5)
      if self.green < (self.GREEN_MAX -5):
        self.green = (self.green + 5)
    else:
      if self.red > (self.RED_MIN - 5):
        self.red = (self.red - 5)
      if self.green > (self.GREEN_MIN -5):
        self.green = (self.green - 5)
    return [self.red, self.green, 0]

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

  RED_MAX = 150
  GREEN_MAX = 40

  RED_MIN = 120
  GREEN_MIN = 10

  def setup(self):
    self.red = 170
    self.green = 20

  def floor(self, prev):
    if randint(0,1) == 1:
      if self.red < (self.RED_MAX - 5):
        self.red = (self.red + 5)
      if self.green < (self.GREEN_MAX -5):
        self.green = (self.green + 5)
    else:
      if self.red > (self.RED_MIN - 5):
        self.red = (self.red - 5)
      if self.green > (self.GREEN_MIN -5):
        self.green = (self.green - 5)
    '''
    if self.count > 100:
      self.red = randint(120,200)
      self.green = randint(10,40)
      self.count = 0
    '''
    return [self.red, self.green, 0]

  def window_top(self, prev):
    return [20, 100, 255]
    #sky blue: return [20, 100, 255]
	#plains grass: return [80, 180, 0] 
	#sandish: return [180, 140, 100]

  def window_bot(self, prev):
    return [100, 50, 20]


