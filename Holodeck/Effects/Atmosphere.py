from Holodeck.Settings import Pipe as P
from Outputs.RGBMultiController import NTOWER, NRING
from Holodeck.Engine import EffectTemplate
from random import randint

class DayEffect(EffectTemplate):
  META = {
    'text': "Daytime",
  }

  def get_mapping(self):
    return {
      P.LIGHTS: (self.lights, 1),
    }

  def lights(self, prev):
    return True

class RainEffect(EffectTemplate):

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


class FireEffect(EffectTemplate):

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

class TorchEffect(EffectTemplate):

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

