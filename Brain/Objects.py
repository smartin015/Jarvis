#!/usr/bin/env python
from JarvisBase import JarvisBase
from Outputs.RGBMultiController import RGBState
import time

class BinaryObject(JarvisBase):
  def __init__(self):
    JarvisBase.__init__(self)
    self.state = 0
  
  def isValid(self, words):
   return ('on' in words) or ('off' in words)
     
  def parse(self, outputs, words):
    outputs['livingroom']['tower'].setState(RGBState.STATE_CHASE)
    t = time.time()
    self.play_sound("confirm.wav")
    if not self.state:
      self.turnOn(outputs)
      self.state = 1
    else:
      self.turnOff(outputs)
      self.state = 0

    while (time.time() - t < 1.0):
      time.sleep(0.1)
    outputs['livingroom']['tower'].defaultState()
      
  def turnOff(self, outputs):
    self.logger.error("TODO: Implement turnOff")

  def turnOn(self, outputs):
    self.logger.error("TODO: Implement turnOn")

class AC(BinaryObject):
  def isValid(self, words):
    return True

  def parse(self, outputs, words):
    outputs['livingroom']['tower'].setState(RGBState.STATE_CHASE)
    self.play_sound("confirm.wav")
    rf = outputs['livingroom']['RF']
    rf.send_IR("AirConditionerPower.txt")
    self.logger.debug("Toggled")
    outputs['livingroom']['tower'].defaultState()

class MainLight(BinaryObject):
  def isValid(self, words):
    return True

  def parse(self, outputs, words):
    outputs['livingroom']['tower'].setState(RGBState.STATE_CHASE)
    self.play_sound("confirm.wav")
    outputs['livingroom']['tracklight'].toggle()
    time.sleep(1.0)
    self.logger.debug("Toggled")
    outputs['livingroom']['tower'].defaultState()
      
class Audio(BinaryObject):
  def isValid(self, words):
    return True

  def turnOff(self, outputs):
    self.chan(1, outputs['livingroom']['RF'])

  def turnOn(self, outputs):
    self.chan(2, outputs['livingroom']['RF'])

  def chan(self, c, rf):
    rf.send_IR("SoundSystemA%d.txt" % c)
    time.sleep(0.5)
    rf.send_IR("SoundSystemB%d.txt" % c)
    time.sleep(0.5)

class AuxProjector(BinaryObject):
  def isValid(self, words):
    return True

  def turnOn(self, outputs):
    self.togglePower(outputs)

  def turnOff(self, outputs):
    self.togglePower(outputs)

  def togglePower(self, outputs):
    rf = outputs['livingroom']['RF']
    rf.send_IR("SideProjectorPower.txt")
    time.sleep(0.5)
    rf.send_IR("SideProjectorPower.txt")
    

class Projector(BinaryObject):
  name = "Projector"

  def isValid(self, words):
    return True

  def parse(self, outputs, words):
    outputs['livingroom']['tower'].setState(RGBState.STATE_CHASE)
    self.play_sound("confirm.wav")

    rf = outputs['livingroom']['RF']

    if "screen" in words:
      # Just do screen, not projector
      if not self.state:
        self.screendown(rf)
      else:
        self.screenup(rf)
    else:
      if not self.state:
        self.turnOn(rf)
      else:
        self.turnOff(rf)
    self.state = 1 - self.state

    outputs['livingroom']['tower'].defaultState()


  def turnOn(self, rf):
    self.logger.info("Pressing power button")
    self.powerbtn(rf)
    self.logger.info("Lowering screen")
    self.screendown(rf)
    self.logger.info("Done")

  def turnOff(self, rf):
    self.logger.info("Pressing power button")
    self.powerbtn(rf)
    self.logger.info("Raising screen")
    self.screenup(rf)
    self.logger.info("Done")

  def screenup(self, rf):
    rf.send_IR("ProjectorScreenStop.txt")
    rf.send_IR("ProjectorScreenUp.txt")

  def screendown(self, rf):
    rf.send_IR("ProjectorScreenStop.txt")
    rf.send_IR("ProjectorScreenDown.txt")

  def powerbtn(self, rf):
    rf.send_IR("ProjectorPower.txt")
    rf.send_IR("ProjectorPower.txt")

