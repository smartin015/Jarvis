from Holodeck.Settings import Pipe as P
from Outputs.RGBMultiController import NTOWER, NRING
from Holodeck.Engine import EffectTemplate
from random import randint

SKY = [20, 100, 205]
SAND = [180, 140, 100]
GRASS = [50, 125, 0]


class ForestEffect(EffectTemplate):
  META = {
    'tab': "locations",
  }

  def get_mapping(self):
    return {
      P.FLOOR: (self.floor, 1),
      P.WINDOWTOP: (self.window_top, 1),
      P.WINDOWBOT: (self.window_bot, 1),
      P.WALLIMG: (self.wall_img, 1),
      P.WINDOWIMG: (self.window_img, 1),
    }

  def floor(self, prev):
    return [102, 55, 0]

  def window_top(self, prev):
    return [55, 185, 55]

  def window_bot(self, prev):
    return [102, 55, 0]

  def wall_img(self, prev):
    return "forest.jpg"

  def window_img(self, prev):
    return "forest.jpg"

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


class DesertEffect(EffectTemplate):
  META = {
    'tab': "locations",
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

