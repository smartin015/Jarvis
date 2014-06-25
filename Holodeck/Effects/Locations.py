from Holodeck.Settings import Pipe as P
from Outputs.RGBMultiController import NTOWER, NRING
from Outputs.ScreenController import ScreenController as scl
from Holodeck.Engine import EffectTemplate, classname_to_id
from random import randint
import time
import inspect
import sys
IMG_PATH = "Holodeck/Images/"
#location_weather_time
#SKY = [20, 100, 205]
SKY = [200, 200, 230]
SAND = [180, 140, 100]
#GRASS = [50, 125, 0]
GRASS = [139, 90, 19]

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

class LocationTemplate(EffectTemplate):
  TRANSITION_TIME = 120
  
  def __init__(self, pipes, active_effects, remove_cb):
    EffectTemplate.__init__(self, pipes, active_effects, remove_cb)
    self.steady_mapping = dict(
      [(k,c[0]) for (k,c) in self.get_mapping().items()]
    )
    self.screen_transition = None
    self.ttop = 0
    self.tbot = 0
    self.tfloor = 0
    self.transition = False
    self.prev_window_bot = None
    self.handle_blacklist()

  def location_mapping(self):
    raise Exception("Unimplemented")

  def linear_blend(self, i, rgb1, rgb2):
    blend_amount = min( float(i) / self.TRANSITION_TIME, 1 )
    return [(a*blend_amount) + (b*(1-blend_amount)) for (a,b) in zip(rgb2, rgb1)]

  def tween_blend(self, i, rgb1, rgb2, rgb3):
    if i < self.TRANSITION_TIME / 2:
      return self.linear_blend(2*i, rgb1, rgb2)
    else:
      return self.linear_blend(2*(i-self.TRANSITION_TIME/2), rgb2, rgb3)

  def trans_floor(self, prev):
    self.tfloor += 1
    if self.prev_window_bot:
      final = self.steady_mapping[P.FLOOR](prev)
      return self.tween_blend(self.tfloor, prev, self.prev_window_bot, final)
    else:
      return prev
  
  def trans_window_top(self, prev):
    self.ttop += 1
    final = self.steady_mapping[P.WINDOWTOP](prev)
    return self.linear_blend(self.ttop, prev, final)
    
  def trans_window_bot(self, prev):
    self.tbot += 1
    mid = self.steady_mapping[P.FLOOR](prev)
    final = self.steady_mapping[P.WINDOWBOT](prev)
    if not self.prev_window_bot:
      self.prev_window_bot = final
    return self.tween_blend(self.tbot, prev, mid, final)

  def handle_screen_transition(self, final):
    try:
      self.screen_transition.next()
      return self.transition_screen
    except StopIteration:
      self.handle_blacklist()
      self.remove_from_pipeline()
      self.transition = True
      self.insert_into_pipeline()
      return final

  def get_blacklist(self):
    cs = inspect.getmembers(sys.modules[__name__], inspect.isclass)    
    result = []
    for n,c in cs:
      if c is LocationTemplate or c is self.__class__:
        continue
      if not issubclass(c, LocationTemplate):
        continue
      result.append(c)
    return result
      

  def trans_audio(self, prev):
    prev[1].append("swoosh")
    return prev
    
  def wall_img_default(self, prev):
    prev[1] = classname_to_id(self.__class__.__name__)
    return prev

  def window_img_default(self, prev):
    prev[1] = classname_to_id(self.__class__.__name__)
    return prev
    
  def audio_default(self, prev):
    prev[0].append(classname_to_id(self.__class__.__name__))
    return prev
  
class ForestEffect(LocationTemplate):

  def get_mapping(self):
    return {
      P.FLOOR: (self.floor, 1),
      P.WINDOWTOP: (self.window_top, 1),
      P.WINDOWBOT: (self.window_bot, 1),
      P.WALLIMG: (self.wall_img_default, 1),
      P.WINDOWIMG: (self.window_img_default, 1),
      P.SOUND: (self.audio_default, 1),
    }

  def floor(self, prev):
    return [102, 55, 0]

  def window_top(self, prev):
    return SKY

  def window_bot(self, prev):
    return [102, 155, 0]

class PlainsEffect(LocationTemplate):

  def get_mapping(self):
    return {
      P.FLOOR: (self.floor, 1),
      P.TOWER: (self.tower, 1),
      P.WINDOWTOP: (self.window_top, 1),
      P.WINDOWBOT: (self.window_bot, 1),
      P.WALLIMG: (self.wall_img_default, 1),
      P.WINDOWIMG: (self.window_img_default, 1),
    }

  def floor(self, prev):
    return GRASS
    #return [255, 255, 0]
    
  def tower(self, prev):
    return [(list(SKY)) for i in xrange(NTOWER)]
    
  def window_top(self, prev):
    return SKY

  def window_bot(self, prev):
    return [0, 128, 0]
    #return [0, 255, 255]

class TundraEffect(LocationTemplate):

  def get_mapping(self):
    return {
      P.FLOOR: (self.floor, 1),
      P.TOWER: (self.tower, 1),
      P.WINDOWTOP: (self.window_top, 1),
      P.WINDOWBOT: (self.window_bot, 1),
      P.WALLIMG: (self.wall_img_default, 1),
      P.WINDOWIMG: (self.window_img_default, 1),
    }

  def floor(self, prev):
    return [255,255,255]
    
  def tower(self, prev):
    return [(list(SKY)) for i in xrange(NTOWER)]

  def window_top(self, prev):
    return SKY

  def window_bot(self, prev):
    return [255,255,255]
    
class RiverEffect(LocationTemplate):


  def get_mapping(self):
    return {
      P.FLOOR: (self.floor, 1),
      P.TOWER: (self.tower, 1),
      P.WINDOWTOP: (self.window_top, 1),
      P.WINDOWBOT: (self.window_bot, 1),
      P.WALLIMG: (self.wall_img_default, 1),
      P.WINDOWIMG: (self.window_img_default, 1),
    }

  def floor(self, prev):
    return [0,0,255]

  def tower(self, prev):
    return [(list(SKY)) for i in xrange(NTOWER)]
    
  def window_top(self, prev):
    return SKY

  def window_bot(self, prev):
    return [0,0,255]
    
    
class DesertEffect(LocationTemplate):

  def get_mapping(self):
    return {
      P.FLOOR: (self.floor, 1),
      P.TOWER: (self.tower, 1),
      P.WINDOWTOP: (self.window_top, 1),
      P.WINDOWBOT: (self.window_bot, 1),
      P.WALLIMG: (self.wall_img_default, 1),
      P.WINDOWIMG: (self.window_img_default, 1),
    }

  def floor(self, prev):
    return SAND
    
  def tower(self, prev):
    return [flicker(list(SKY)) for i in xrange(NTOWER)]

  def window_top(self, prev):
    return flicker(list(SKY))

  def window_bot(self, prev):
    return SAND




    
class WaterEffect(LocationTemplate):

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
      P.WALLIMG: (self.wall_img_default, 1),
      P.WINDOWIMG: (self.window_img_default, 1),
    }



  def floor(self, prev):
    return [0,0,255]

  def window_top(self, prev):
    return SKY

  def window_bot(self, prev):
    return [0,0,255]
50 
class JungleEffect(LocationTemplate):

  def get_mapping(self):
    return {
      P.FLOOR: (self.floor, 1),
      P.WINDOWTOP: (self.window_top, 1),
      P.WINDOWBOT: (self.window_bot, 1),
      P.WALLIMG: (self.wall_img_default, 1),
      P.WINDOWIMG: (self.window_img_default, 1),
    }

  def floor(self, prev):
    return [102, 55, 0]

  def window_top(self, prev):
    return [0, 125, 0]

  def window_bot(self, prev):
    return [0, 125, 0]

class BeachEffect(LocationTemplate): 

  def tower(self, prev):
    return [(list(SKY)) for i in xrange(NTOWER)]


  def get_mapping(self):
    return {
      P.FLOOR: (self.floor, 1),
      P.TOWER: (self.tower, 1),
      P.WINDOWTOP: (self.window_top, 1),
      P.WINDOWBOT: (self.window_bot, 1),
      P.WALLIMG: (self.wall_img_default, 1),
      P.WINDOWIMG: (self.window_img_default, 1),
    }

  def floor(self, prev):
    return SAND

  def window_top(self, prev):
    return SKY

  def window_bot(self, prev):
    return SAND

class MountainEffect(LocationTemplate):

  def get_mapping(self):
    return {
      P.FLOOR: (self.floor, 1),
      P.TOWER: (self.tower, 1),
      P.WINDOWTOP: (self.window_top, 1),
      P.WINDOWBOT: (self.window_bot, 1),
      P.WALLIMG: (self.wall_img_default, 1),
      P.WINDOWIMG: (self.window_img_default, 1),
    }

  def floor(self, prev):
    return [255,255,255]
    
  def tower(self, prev):
    return [(list(SKY)) for i in xrange(NTOWER)]

  def window_top(self, prev):
    return SKY

  def window_bot(self, prev):
    return [255,255,255]
