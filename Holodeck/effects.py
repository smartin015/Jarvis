from pipe import Pipe as P
from Outputs.RGBMultiController import NTOWER, NRING
from Holodeck.effect_template import EffectTemplate
from random import randint

SKY = [20, 100, 205]
SAND = [180, 140, 100]
GRASS = [50, 125, 0]

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
    return [102, 55, 0]

  def window_top(self, prev):
    return [55, 185, 55]

  def window_bot(self, prev):
    return [102, 55, 0]

def flicker(rgb, flicker = 3):
  randomNum = randint(0,2)

  if randomNum == 0:
    if rgb[0] <= 255 - flicker:
      rgb[0] = rgb[0] + flicker
    if rgb[1] <= 255 - flicker:
      rgb[1] = rgb[1] + flicker
    if rgb[2] <= 255 - flicker:
      rgb[2] = rgb[2] + flicker
  elif randomNum == 1:
    if rgb[0] > 0 + flicker:
      rgb[0] = rgb[0] - flicker
    if rgb[1] > 0 + flicker:
      rgb[1] = rgb[1] - flicker
    if rgb[2] > 0 + flicker:
      rgb[2] = rgb[2] - flicker

  return rgb
    

class RainEffect(EffectTemplate):
  META = {
    'tab': "atmosphere",
    'text': "Rain",
  }

  def setup(self):
    self.count = 0
    self.arrcount = 0
    self.towerRGB = [[0, 0, 0] for i in xrange(NTOWER)]

  def get_mapping(self): 
    return {
      P.TOWER: (self.tower, 1),
      P.RING: (self.ring, 1),
    }

  def tower(self, prev):
    for x in self.towerRGB:
      if x[2] > 0:
        x[2] = (x[2] - 5)
      else:
        if randint(1,200) == 5:
          x[2] = 150
    
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
      P.LIGHTS: (self.lights, 1),
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
    self.increment = 1
    self.count = 0;

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
  META = {
    'tab': "effects",
    'text': "Paul-ify",
  }

  def get_mapping(self):
    return {
      P.FLOOR: (self.floor, 1),
      P.WINDOWTOP: (self.window_top, 1),
      P.WINDOWBOT: (self.window_bot, 1),
      P.SOUND: (self.audio, 1),
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

  def audio(self, prev):
    return ['confirm']

  def window_top(self, prev):
    return [20, 100, 255]
    #sky blue: return [20, 100, 255]
	#plains grass: return [80, 180, 0] 
	#sandish: return [180, 140, 100]

  def window_bot(self, prev):
    return [100, 50, 20]

class CandleEffect(EffectTemplate):
  META = {
    'tab': "effects",
    'text': "Fire",
  }

  def get_mapping(self):
    return {
      P.RING: (self.ring, 1),
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

class LightningEffect(EffectTemplate):
  META = {
    'tab': "atmosphere",
    'text': "Lightning",
  }

  def setup(self):
    self.count = 0
    self.towerRGBON = [[80, 80, 255]]*NTOWER
    self.towerRGBOFF = [[0, 0, 0]]*NTOWER

  def get_mapping(self): 
    return {
      P.TOWER: (self.tower, 1),
      P.RING: (self.ring, 1),
      P.SOUND: (self.audio, 1),
    }

  def tower(self, prev):
    '''
    for x in self.towerRGB:
          x[0] = 80
          x[1] = 80
          x[2] = 255
    

    if self.count >= len(self.lightningarr):
      self.remove()
      return self.towerRGBOFF
    if self.count%2 == 0:
      if self.sentinel < self.lightningarr[self.count]:
        self.sentinel = (self.sentinel + 1)
        return self.towerRGBON
      else:
        self.sentinel = 0
        self.count = (self.count + 1)
    else:
      if self.sentinel < self.lightningarr[self.count]:
        self.sentinel = (self.sentinel + 1)
        return self.towerRGBOFF
      else:
        self.sentinel = 0
        self.count = (self.count + 1)
        '''
    if self.shouldLightning():
      return self.towerRGBON
    else:
      return self.towerRGBOFF

    

  def shouldLightning(self):
    
    if self.count%2 == 0:
      return True
    else:
      return False

  def post_render(self):
    self.count += 1

    if self.count >= 12 or self.should_exit:
      self.remove()
      

  def ring(self, prev):
    return [[0, 0, 0]]*NRING
  
  def audio(self, prev):
    #prev.append('thunder')
    return ['thunder']
  
class DesertEffect(EffectTemplate):
  META = {
    'tab': "locations",
    'text': "Desert",
  }

  def tower(self, prev):
    return [flicker(list(SKY)) for i in xrange(NTOWER)]


  def get_mapping(self):
    return {
      P.FLOOR: (self.floor, 1),
      P.TOWER: (self.tower, 1),
      P.WINDOWTOP: (self.window_top, 1),
      P.WINDOWBOT: (self.window_bot, 1),
    }

  def floor(self, prev):
    return SAND

  def window_top(self, prev):
    return flicker(list(SKY))

  def window_bot(self, prev):
    return SAND

class TundraEffect(EffectTemplate):
  META = {
    'tab': "locations",
    'text': "Tundra",
  }

  def tower(self, prev):
    return [(list(SKY)) for i in xrange(NTOWER)]


  def get_mapping(self):
    return {
      P.FLOOR: (self.floor, 1),
      P.TOWER: (self.tower, 1),
      P.WINDOWTOP: (self.window_top, 1),
      P.WINDOWBOT: (self.window_bot, 1),
    }

  def floor(self, prev):
    return [255,255,255]

  def window_top(self, prev):
    return SKY

  def window_bot(self, prev):
    return [255,255,255]

class WaterEffect(EffectTemplate):
  META = {
    'tab': "locations",
    'text': "water",
  }

  def setup(self):
    self.count = 0

  def tower(self, prev):
    return [(list(SKY)) for i in xrange(NTOWER)]


  def get_mapping(self):
    return {
      P.FLOOR: (self.floor, 1),
      P.TOWER: (self.tower, 1),
      P.WINDOWTOP: (self.window_top, 1),
      P.WINDOWBOT: (self.window_bot, 1),
    }



  def floor(self, prev):
    return [0,0,255]

  def window_top(self, prev):
    return SKY

  def window_bot(self, prev):
    return [0,0,255]

class JungleEffect(EffectTemplate):
  META = {
    'tab': "locations",
    'text': "Jungle",
  }

  def get_mapping(self):
    return {
      P.FLOOR: (self.floor, 1),
      P.WINDOWTOP: (self.window_top, 1),
      P.WINDOWBOT: (self.window_bot, 1),
    }

  def floor(self, prev):
    return [102, 55, 0]

  def window_top(self, prev):
    return [0, 125, 0]

  def window_bot(self, prev):
    return [0, 125, 0]

class PlainsEffect(EffectTemplate):
  META = {
    'tab': "locations",
    'text': "Plains",
  }

  def tower(self, prev):
    return [(list(SKY)) for i in xrange(NTOWER)]


  def get_mapping(self):
    return {
      P.FLOOR: (self.floor, 1),
      P.TOWER: (self.tower, 1),
      P.WINDOWTOP: (self.window_top, 1),
      P.WINDOWBOT: (self.window_bot, 1),
    }

  def floor(self, prev):
    return GRASS

  def window_top(self, prev):
    return SKY

  def window_bot(self, prev):
    return GRASS

class BeachEffect(EffectTemplate):
  META = {
    'tab': "locations",
    'text': "Beach",
  }

  def tower(self, prev):
    return [(list(SKY)) for i in xrange(NTOWER)]


  def get_mapping(self):
    return {
      P.FLOOR: (self.floor, 1),
      P.TOWER: (self.tower, 1),
      P.WINDOWTOP: (self.window_top, 1),
      P.WINDOWBOT: (self.window_bot, 1),
    }

  def floor(self, prev):
    return SAND

  def window_top(self, prev):
    return SKY

  def window_bot(self, prev):
    return SAND

