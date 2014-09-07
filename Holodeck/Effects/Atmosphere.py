from Holodeck.Settings import Pipe as P
from Outputs.RGBMultiController import NTOWER, NRING
from Holodeck.Engine import EffectTemplate, classname_to_id
from random import randint
import inspect
import sys

class TimeTemplate(EffectTemplate): 
  def __init__(self, pipes, active_effects, remove_cb):
    EffectTemplate.__init__(self, pipes, active_effects, remove_cb)
    self.handle_blacklist()

  def get_blacklist(self):
    cs = inspect.getmembers(sys.modules[__name__], inspect.isclass)    
    result = []
    for n,c in cs:
      if c is TimeTemplate or c is self.__class__:
        continue
      if not issubclass(c, TimeTemplate):
        continue
      result.append(c)
    print "Time blacklist", result
    return result
    
  def wall_img_default(self, prev):
    prev[2] = classname_to_id(self.__class__.__name__)
    return prev

  def window_img_default(self, prev):
    prev[2] = classname_to_id(self.__class__.__name__)
    return prev

  def darken(self, prev, amt):
    if prev and type(prev[0]) is list:
      return [self.darken(p, amt) for p in prev]
    return [int(p*amt) for p in prev]

class WeatherTemplate(EffectTemplate):
  def __init__(self, pipes, active_effects, remove_cb):
    EffectTemplate.__init__(self, pipes, active_effects, remove_cb)
    self.handle_blacklist()

  def get_blacklist(self):
    cs = inspect.getmembers(sys.modules[__name__], inspect.isclass)    
    result = []
    for n,c in cs:
      if c is WeatherTemplate or c is self.__class__:
        continue
      if not issubclass(c, WeatherTemplate):
        continue
      result.append(c)
    return result
    
  def wall_img_default(self, prev):
    prev[1] = classname_to_id(self.__class__.__name__)
    return prev

  def window_img_default(self, prev):
    prev[1] = classname_to_id(self.__class__.__name__)
    return prev


class DayEffect(TimeTemplate):
  META = {
    'text': "Daytime",
  }

  def get_mapping(self):
    return {
      P.LIGHTS: (self.lights, 10),
      P.WALLIMG: (self.wall_img_default, 1),
      P.WINDOWIMG: (self.window_img_default, 1),
    }

  def lights(self, prev):
    return True

class NightEffect(TimeTemplate):
  DARK = 0.1

  def get_mapping(self):
    return {
      P.LIGHTS: (self.lights, 10),
      P.WALLIMG: (self.wall_img_default, 1),
      P.WINDOWIMG: (self.window_img_default, 1),
      P.FLOOR: (self.floor, 10),
      P.TOWER: (self.tower, 10),
      P.WINDOWTOP: (self.window_top, 10),
      P.WINDOWBOT: (self.window_bot, 10),
      P.RING: (self.ring, 10),
    }

  def lights(self, prev):
    return False

  def window_top(self, prev):
    return self.darken(prev, self.DARK)

  def window_bot(self, prev):
    return [0]*3

  def floor(self, prev):
    return [0]*3

  def tower(self, prev):
    return self.darken(prev, self.DARK)

  def ring(self, prev):
    return [[100, 100, 255]]*NRING


class DawnEffect(TimeTemplate):
  DARK = 0.5
  DAWN_SKY = [50, 50, 100]

  def get_mapping(self):
    return {
      P.LIGHTS: (self.lights, 10),
      P.WALLIMG: (self.wall_img_default, 1),
      P.WINDOWIMG: (self.window_img_default, 1),
      P.FLOOR: (self.floor, 10),
      P.TOWER: (self.tower, 10),
      P.WINDOWTOP: (self.window_top, 10),
      P.WINDOWBOT: (self.window_bot, 10),
      P.RING: (self.ring, 10),
    }

  def lights(self, prev):
    return False

  def window_top(self, prev):
    return self.DAWN_SKY

  def window_bot(self, prev):
    return self.darken(prev, self.DARK)

  def floor(self, prev):
    return self.darken(prev, self.DARK)

  def tower(self, prev):
    return self.darken(prev, self.DARK)

  def ring(self, prev):
    return [self.DAWN_SKY]*NRING

class DuskEffect(TimeTemplate):
  DARK = 0.5
  DUSK_SKY = [250, 100, 100]

  def get_mapping(self):
    return {
      P.LIGHTS: (self.lights, 10),
      P.WALLIMG: (self.wall_img_default, 1),
      P.WINDOWIMG: (self.window_img_default, 1),
      P.FLOOR: (self.floor, 10),
      P.TOWER: (self.tower, 10),
      P.WINDOWTOP: (self.window_top, 10),
      P.WINDOWBOT: (self.window_bot, 10),
      P.RING: (self.ring, 10),
    }

  def lights(self, prev):
    return False

  def window_top(self, prev):
    return self.DUSK_SKY

  def window_bot(self, prev):
    return self.darken(prev, self.DARK)

  def floor(self, prev):
    return self.darken(prev, self.DARK)

  def tower(self, prev):
    return self.darken(prev, self.DARK)

  def ring(self, prev):
    return [self.DUSK_SKY]*NRING

class RainEffect(WeatherTemplate):

  def setup(self):
    self.count = 0
    self.arrcount = 0
    self.towerRGB = [[0, 0, 0] for i in xrange(NTOWER)]

  def get_mapping(self): 
    return {
      P.TOWER: (self.tower, 50),
      P.RING: (self.ring, 50),
      P.WALLIMG: (self.wall_img_default, 1),
      P.WINDOWIMG: (self.window_img_default, 1),
      P.WINDOWTOP: (self.window_top, 50),
      P.LIGHTS: (self.lights, 50),
      P.SOUND: (self.sound, 50),
    }

  def window_top(self, prev):
    if (prev[2] < 200):
      prev[2] += 50
    return prev


  def tower(self, prev):
    for x in self.towerRGB:
      if x[2] > 0:
        x[2] = (x[2] - 5)
      else:
        if randint(1,200) == 5:
          x[2] = 150
    
    return self.towerRGB

  def ring(self, prev):
    return [[55, 55, 55]]*NRING

  def wallimg(self, prev):
    prev[2] = "rain"  
    return prev

  def lights(self, prev):
    return False
  
  def sound(self, prev):
    prev[0].append("rain")
    return prev

class FireEffect(EffectTemplate):

  def get_mapping(self):
    return {
      P.FLOOR: (self.floor, 50),
      P.SOUND: (self.sound, 50),
    } 

  RED_MAX = 150
  GREEN_MAX = 40

  RED_MIN = 120
  GREEN_MIN = 10

  def setup(self):
    self.red = 170
    self.green = 20
    self.increment = 1
    self.count = 0;

  def sound(self, prev):
    prev[0].append("fire")
    return prev
    
  def floor(self, prev):
    if self.count < 50:
      if self.red < (self.RED_MAX - self.increment):
        self.red = (self.red + self.increment)
      if self.green < (self.GREEN_MAX -self.increment):
        self.green = (self.green + self.increment)
    else:
      if self.red > (self.RED_MIN - self.increment):
        self.red = (self.red - self.increment)
      if self.green > (self.GREEN_MIN -self.increment):
        self.green = (self.green - self.increment)
    return [self.red, self.green, 0]

class PaulEffect(EffectTemplate):

  def get_mapping(self):
    return {
      P.FLOOR: (self.floor, 500),
      P.WINDOWTOP: (self.window_top, 500),
      P.WINDOWBOT: (self.window_bot, 500),
      P.SOUND: (self.audio, 500),
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

  def audio(self, prev):
    return ['confirm']

  def window_top(self, prev):
    return [20, 100, 255]
    #sky blue: return [20, 100, 255]
	#plains grass: return [80, 180, 0] 
	#sandish: return [180, 140, 100]

  def window_bot(self, prev):
    return [100, 50, 20]

class TorchEffect(EffectTemplate):

  def get_mapping(self):
    return {
      P.RING: (self.ring, 50),
    } 

  RED_MAX = 150
  GREEN_MAX = 40

  RED_MIN = 120
  GREEN_MIN = 10

  def setup(self):
    self.red = 170
    self.green = 20
    self.ringRGB = [[0, 0, 0]]*NRING

  def ring(self, prev):
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
    
    self.ringRGB[0][0] = self.red
    self.ringRGB[0][1] = self.green
    self.ringRGB[0][2] = 0

    return self.ringRGB

