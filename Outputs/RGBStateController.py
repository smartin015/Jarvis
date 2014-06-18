import threading
import time
from Queue import Queue

class RGBState():
  STATE_OFF = 0
  STATE_LIGHT = 1
  STATE_FADE = 2
  STATE_CHASE = 3
  STATE_FLASH = 4
  STATE_TRIWIPE = 5
  STATE_RAINBOW = 6
  STATE_RAINBOWCHASE = 7
  STATE_PARTY = 8

class RGBStateController(threading.Thread):
  def __init__(self, ser, default = None):
    threading.Thread.__init__(self)
    self.ser = ser
    self.ser.open()
    self.buf = Queue()
    self.daemon = True
    self.default = default
    self.start()

  def __del__(self):
    self.ser.close()

  def setDefault(self, state):
    self.default = state

  def run(self):
    while True:
      if self.buf.empty() and self.default is not None:
        self.ser.write(chr(self.default))

      (state, duration) = self.buf.get(block=True, timeout=None)
      print "WRITING %d" % state
      self.ser.write(chr(state))
      time.sleep(duration)

  def queueState(self, state, duration):
    self.buf.put((state, duration))

if __name__ == "__main__":
  import serial
  ser = serial.Serial("/dev/ttyACM0", 9600)
  ser.close()


  con = RGBController(ser)

  while True:
    sstr = raw_input("State: ")
    
    for s in sstr:
      con.queueState(int(s), 1.0)
    
