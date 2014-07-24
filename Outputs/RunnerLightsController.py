from Controller import Controller
import threading
import time



class RunnerLightsController(Controller):
  MAX_LEVEL = 128
  MIN_LEVEL = 0
  TIMEOUT = 10.0
  TRANSITION_TIME = 3.0
  LIGHT_THRESH = 300

  def __init__(self, motion_ser):
    Controller.__init__(self)
    self.ser = motion_ser
    self.on = False

  def enable(self, rf):
    self.rf = rf
    self.rf.send_cmd(self.rf.CMD_FET1, self.MIN_LEVEL, "hackspace")
    self.logger.debug("Reset runners to MIN_LEVEL")
    t = threading.Thread(target=self.light_control)
    t.daemon = True
    t.start()

  def motion_sense(self, timeout=None):
    self.ser.timeout = timeout
    try:
      l = self.ser.readline().strip()
      (onoff, light) = l.split(" ")
      onoff = (onoff == "1")
      return (onoff, int(light))
    except ValueError:
      return (None, None)
  
  def fade(self, base, delta):
    start = time.time()
    cutoff = start + self.TRANSITION_TIME
    while time.time() < cutoff:
      offs = ((time.time() - start) / self.TRANSITION_TIME) * delta
      self.rf.send_cmd(self.rf.CMD_FET1, int(base + offs), "hackspace")
      time.sleep(0.02)

  def fade_in(self):
    if self.on:
      return

    self.logger.debug("Fading in")
    delta = self.MAX_LEVEL - self.MIN_LEVEL
    self.fade(self.MIN_LEVEL, delta)
    self.on = True

  def fade_out(self):
    if not self.on:
      return

    self.logger.debug("Fading out")
    delta = self.MIN_LEVEL - self.MAX_LEVEL
    self.fade(self.MAX_LEVEL, delta)
    self.on = False

  def light_control(self):
    self.logger.debug("Runner lights controller started")
    while True:
      (motion, light) = self.motion_sense()
      while self.ser.inWaiting() > 0:
        (motion, light) = self.motion_sense()

      if motion and light < self.LIGHT_THRESH:
        self.fade_in()

        # Time delay to ensure stays on
        while True:
          (motion, light) = self.motion_sense(self.TIMEOUT)
          if motion is None:
            break

      # We'll have to fade out either way
      self.fade_out()


if __name__ == "__main__":
  import serial
  from Inputs.USBDiscovery import get_connected_usb_devices
  from Outputs.RFController import RFController
  import logging

  logging.basicConfig()
  MOTION_ID = "A602KAB4"
  RF_ID = "A9MDTZJF"
  devices = get_connected_usb_devices()

  motion_ser = serial.Serial(devices[MOTION_ID], 9600)
  rf = RFController(serial.Serial(devices[RF_ID], 115200), "hackspace")
  time.sleep(1.0)

  con = RunnerLightsController(motion_ser)
  con.enable(rf)
  raw_input("Enter to exit")
