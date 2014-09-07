#!/usr/bin/env python
from JarvisBase import JarvisBase
from Outputs.RGBMultiController import RGBState
from Outputs.Controller import send_cmd
import time
import datetime
from config import RF
import random

NOVOICE_END = datetime.time(9,0)
NOVOICE_BEGIN = datetime.time(23,0)

class CommandObject(JarvisBase):
  RESPONSES = ["confirm.wav", "confirm2.wav"]

  def isValid(self, words):
    return True

  def handle(self, words, origin):
    self.init_response(origin)
    self.parse(words, origin)
    self.end_response(origin)

  def init_response(self, origin):
    send_cmd('tower', 'setState', [RGBState.STATE_CHASE])
    self.response_start_time = time.time()
    now = datetime.datetime.now().time()
    if origin != 'console' and now > NOVOICE_END and now < NOVOICE_BEGIN:
      send_cmd('speaker', 'play_sound', ['confirm.wav'])
  
  def end_response(self, origin):
    while (time.time() - self.response_start_time < 1.0):
      time.sleep(0.1)
    send_cmd('tower', 'defaultState')

  def parse(self, words, origin):
    raise Exception("unimplemented")

class ToggleObject(CommandObject):

  def parse(self, words, origin):
    self.toggle(words, origin)
    self.logger.debug("Toggled")

  def toggle(self, words, origin):
    raise Exception("Unimplemented")

class BinaryObject(CommandObject):
  ON = "on"
  OFF = "off"

  def __init__(self):
    CommandObject.__init__(self)
    self.state = self.OFF
  
  def setState(self, state, words, origin):
    if state == self.ON:
      if self.state == self.OFF:
        self.turnOn(words, origin)
        self.state = self.ON
      else:
        self.logger.info("Already on")
    elif state == self.OFF:
      if self.state == self.ON:
        self.turnOff(words, origin)
        self.state = self.OFF
      else:
        self.logger.info("Already off")
    else:
      raise Exception("Invalid state")

  def getState(self):
    return self.state

  def parse(self, words, origin):
    if self.state == self.OFF:
      self.turnOn(words, origin)
      self.state = self.ON
    else:
      self.turnOff(words, origin)
      self.state = self.OFF
      
  def turnOff(self, words, origin):
    raise Exception("Unimplemented")

  def turnOn(self, words, origin):
    raise Exception("Unimplemented")

class AC(ToggleObject):
  def toggle(self, words, origin):
    send_cmd('RF', 'send_IR', ["AirConditionerPower.txt"])
    pass
      
class Audio(BinaryObject):
  def turnOff(self, words, origin):
    self.chan(1)

  def turnOn(self, words, origin):
    self.chan(2)

  def chan(self, c):
    send_cmd('RF', 'send_IR', ["SoundSystemA%d.txt" % c])
    time.sleep(0.5)

    send_cmd('RF', 'send_IR', ["SoundSystemB%d.txt" % c])
    time.sleep(0.5)

class AuxProjector(BinaryObject):
  def toggle(self, words, origin):
    send_cmd('RF', 'send_IR', ["SideProjectorPower.txt"])
    time.sleep(0.5)
    send_cmd('RF', 'send_IR', ["SideProjectorPower.txt"])

  def turnOn(self, words, origin):
    self.toggle(words, origin)

  def turnOff(self, words, origin):
    self.toggle(words, origin)

class Projector(BinaryObject):
  def parse(self, words, origin):

    if "screen" in words:
      # Just do screen, not projector
      if self.state == self.OFF:
        self.screendown()
        self.state = self.ON
      else:
        self.screenup()
        self.state = self.OFF
    else:
      if self.state == self.OFF:
        self.turnOn(words, origin)
        self.state = self.ON
      else:
        self.turnOff(words, origin)
        self.state = self.OFF

  def turnOn(self, words, origin):
    self.logger.info("Pressing power button")
    self.powerbtn()
    self.logger.info("Lowering screen")
    self.screendown()
    self.logger.info("Done")

  def turnOff(self, words, origin):
    self.logger.info("Pressing power button")
    self.powerbtn()
    self.logger.info("Raising screen")
    self.screenup()
    self.logger.info("Done")

  def screenup(self):
    send_cmd('RF', 'send_IR', ["ProjectorScreenStop.txt"])
    send_cmd('RF', 'send_IR', ["ProjectorScreenUp.txt"])


  def screendown(self):
    send_cmd('RF', 'send_IR', ["ProjectorScreenStop.txt"])
    send_cmd('RF', 'send_IR', ["ProjectorScreenDown.txt"])

  def powerbtn(self):
    send_cmd('RF', 'send_IR', ["ProjectorPower.txt"])
    send_cmd('RF', 'send_IR', ["ProjectorPower.txt"])

class MainLight(BinaryObject):
  def __init__(self):
    BinaryObject.__init__(self)
    self.hacklight = False

  def turnOn(self, words, origin):
    self.toggle(words, origin)

  def turnOff(self, words, origin):
    self.toggle(words, origin)

  def toggle(self, words, origin):
    if origin in ["livingroom", "console"]:
      send_cmd('tracklight', 'toggle')
    elif origin == "hackspace" or "hack" in words:
      self.toggle_hacklight()

  def toggle_hacklight(self):
    val = 255 if self.hacklight else 0
    send_cmd('RF', 'send_cmd', [RFController.FET1, val, RF["hackspace"]])
    self.hacklight = not self.hacklight

