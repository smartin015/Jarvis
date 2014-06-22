from Holodeck.Settings import Pipe as P
from Outputs.RGBMultiController import NTOWER, NRING
from Outputs.ScreenController import ScreenController as scl
from Holodeck.Engine import EffectTemplate
from random import randint
import time

SKY = [20, 100, 205]
SAND = [180, 140, 100]
GRASS = [50, 125, 0]


class LocationEffect(EffectTemplate):
  TRANSITION_TIME = 1000

  def setup(self):
    self.steady_mapping = dict(
      [(k,c[0]) for (k,c) in self.get_mapping().items()]
    )
    self.sweep = None
    self.transition_screen = scl.get_black_image()
    self.ttop = 0
    self.transition = False

  def location_mapping(self):
    raise Exception("Unimplemented")

  def trans_floor(self, prev):
    return prev
  
  def trans_window_top(self, prev):
    self.ttop += 1
    final = self.steady_mapping[P.WINDOWTOP](prev)
    blend_amount = self.ttop / self.TRANSITION_TIME
    return [(a*blend_amount) + (b*(1-blend_amount)) for (a,b) in zip(final, prev)]
    
  def trans_window_bot(self, prev):
    return prev

  def trans_wall_img(self, screen):
    final = self.steady_mapping[P.WALLIMG](screen)
    if not self.sweep:
      self.sweep = scl.gen_sweep(screen, final, self.transition_screen)

    try:
      self.sweep.next()
      return self.transition_screen
    except StopIteration:
      self.remove_from_pipeline()
      self.transition = True
      self.insert_into_pipeline()
      return final

  def trans_window_img(self, screen):
    return screen

  def _get_mapping(self): 
    if not self.transition:
      priorities = dict([(k,c[1]) for (k,c) in self.get_mapping().items()])
      return {
        P.FLOOR: (self.trans_floor, priorities[P.FLOOR]),
        P.WINDOWTOP: (self.trans_window_top, priorities[P.WINDOWTOP]),
        P.WINDOWBOT: (self.trans_window_bot, priorities[P.WINDOWBOT]),
        P.WALLIMG: (self.trans_wall_img, priorities[P.WALLIMG]),
        P.WINDOWIMG: (self.trans_window_img, priorities[P.WINDOWIMG]),
        #TODO: Other effects
      }
    else:
      return self.get_mapping()


class ForestEffect(LocationEffect):

  def setup(self):
    LocationEffect.setup(self)
    self.forest_screen = scl.loadimg("Holodeck/Images/forest.jpg")

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
    return self.forest_screen

  def window_img(self, prev):
    return self.forest_screen

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
    


class DesertEffect(EffectTemplate):

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

