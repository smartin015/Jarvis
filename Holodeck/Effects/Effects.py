from Holodeck.Settings import Pipe as P
from Outputs.RGBMultiController import NTOWER, NRING
from Holodeck.Engine import EffectTemplate
from random import randint

class BattleEffect(EffectTemplate):

  def get_mapping(self):
    return {
      P.WINDOWTOP: (self.window_top, 1),
      P.WINDOWBOT: (self.window_bot, 1)
    }

  def window_top(self, prev):
    return [255, 0, 0]

  def window_bot(self, prev):
    return [255, 0, 0]

class LightningEffect(EffectTemplate):

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


    self.count += 1
    if self.count >= 12 or self.should_exit:
      self.remove()

    if self.shouldLightning():
      return self.towerRGBON
    else:
      return self.towerRGBOFF

  def shouldLightning(self):
    
    if self.count%2 == 0:
      return True
    else:
      return False


  def ring(self, prev):
    return [[0, 0, 0]]*NRING
  
  def audio(self, prev):
    #prev.append('thunder')
    return ['thunder']
  

