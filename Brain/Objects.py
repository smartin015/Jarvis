#!/usr/bin/env python
from JarvisBase import JarvisBase
from Outputs.RGBMultiController import RGBState
import time
from config import RF

class ToggleObject(JarvisBase):
  def isValid(self, words):
    return True

  def parse(self, outputs, words, origin):
    outputs['tower'].setState(RGBState.STATE_CHASE)
    t = time.time()

    if origin != 'console':
      self.play_sound("confirm.wav")

    self.toggle(outputs, words, origin)
    self.logger.debug("Toggled")

    while (time.time() - t < 1.0):
      time.sleep(0.1)
    outputs['tower'].defaultState()

  def toggle(self, outputs, words, origin):
    raise Exception("Unimplemented")

class BinaryObject(JarvisBase):
  ON = "on"
  OFF = "off"

  def __init__(self):
    JarvisBase.__init__(self)
    self.state = self.OFF
  
  def isValid(self, words):
   return True
  
  def setState(self, state, outputs, words, origin):
    if state == self.ON:
      if self.state == self.OFF:
        self.turnOn(outputs, words, origin)
        self.state = self.ON
      else:
        self.logger.info("Already on")
    elif state == self.OFF:
      if self.state == self.ON:
        self.turnOff(outputs, words, origin)
        self.state = self.OFF
      else:
        self.logger.info("Already off")
    else:
      raise Exception("Invalid state")

  def getState(self):
    return self.state

  def parse(self, outputs, words, origin):
    outputs['tower'].setState(RGBState.STATE_CHASE)
    t = time.time()

    if origin != 'console':
      self.play_sound("confirm.wav")

    if self.state == self.OFF:
      self.turnOn(outputs, words, origin)
      self.state = self.ON
    else:
      self.turnOff(outputs, words, origin)
      self.state = self.OFF

    while (time.time() - t < 1.0):
      time.sleep(0.1)
    outputs['tower'].defaultState()
      
  def turnOff(self, outputs, words, origin):
    raise Exception("Unimplemented")

  def turnOn(self, outputs, words, origin):
    raise Exception("Unimplemented")

class AC(ToggleObject):
  def toggle(self, outputs, words, origin):
    outputs['RF'].send_IR("AirConditionerPower.txt")
      
class Audio(BinaryObject):
  def turnOff(self, outputs, words, origin):
    self.chan(1, outputs['RF'])

  def turnOn(self, outputs, words, origin):
    self.chan(2, outputs['RF'])

  def chan(self, c, rf):
    rf.send_IR("SoundSystemA%d.txt" % c)
    time.sleep(0.5)
    rf.send_IR("SoundSystemB%d.txt" % c)
    time.sleep(0.5)

class AuxProjector(BinaryObject):
  def toggle(self, outputs, words, origin):
    rf = outputs['RF']
    rf.send_IR("SideProjectorPower.txt")
    time.sleep(0.5)
    rf.send_IR("SideProjectorPower.txt")

  def turnOn(self, outputs, words, origin):
    self.toggle(outputs, words, origin)

  def turnOff(self, outputs, words, origin):
    self.toggle(outputs, words, origin)

class Projector(BinaryObject):
  def parse(self, outputs, words, origin):
    outputs['tower'].setState(RGBState.STATE_CHASE)
    self.play_sound("confirm.wav")

    rf = outputs['RF']

    if "screen" in words:
      # Just do screen, not projector
      if self.state == self.OFF:
        self.screendown(rf)
        self.state = self.ON
      else:
        self.screenup(rf)
        self.state = self.OFF
    else:
      if self.state == self.OFF:
        self.turnOn(outputs, words, origin)
        self.state = self.ON
      else:
        self.turnOff(outputs, words, origin)
        self.state = self.OFF

    outputs['tower'].defaultState()

  def turnOn(self, outputs, words, origin):
    rf = outputs['RF']
    self.logger.info("Pressing power button")
    self.powerbtn(rf)
    self.logger.info("Lowering screen")
    self.screendown(rf)
    self.logger.info("Done")

  def turnOff(self, outputs, words, origin):
    rf = outputs['RF']
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

class MainLight(BinaryObject):
  def __init__(self):
    BinaryObject.__init__(self)
    self.hacklight = False

  def turnOn(self, outputs, words, origin):
    self.toggle(outputs, words, origin)

  def turnOff(self, outputs, words, origin):
    self.toggle(outputs, words, origin)

  def toggle(self, outputs, words, origin):
    if origin == "livingroom":
      outputs['tracklight'].toggle()
    elif origin == "hackspace" or "hack" in words:
      self.toggle_hacklight(outputs)

  def toggle_hacklight(self, outputs):
    val = 255 if self.hacklight else 0
    outputs['RF'].send_cmd(RFController.FET1, val, RF["hackspace"])
    self.hacklight = not self.hacklight

