import time
import threading
from Controller import Controller

NTOWER = 105
NRING = 24

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
  STATE_ERROR = 9
  STATE_MANUAL = 10

  CMD_UPDATE = 0xff
  CMD_EXIT_MANUAL = 0xfe

class RGBMultiController(Controller):
  def __init__(self, ser, default = RGBState.STATE_OFF):
    Controller.__init__(self)
    self.ser = ser
    self.default = default
    self.keepalive = False
    self.state = self.default
    self.lock = threading.Lock()

  def __del__(self):
    self.ser.close()

  def setDefault(self, state, keepalive=False):
    self.default = state

    self.lock.acquire()
    if keepalive and not self.keepalive:
      self.keepalive = keepalive
      self.state = self.default
      self.logger.debug("Starting RGB keepalive thread")
      t = threading.Thread(target=self.run_keepalive)
      t.daemon = True
      t.start()
    else:
      self.keepalive = keepalive
    self.lock.release()

  def run_keepalive(self):
    while self.keepalive:
      try:
        self.setState(self.state)
        self.logger.debug("Update Tower RGB")
      except:
        self.logger.warn("Couldn't update tower RGB")
      time.sleep(20.0)
    self.logger.debug("RGB Keepalive exiting")

  def defaultState(self):
    self.setState(self.default)

  def setState(self, state):
    self.state = state
    self.ser.write(chr(state))
    assert(self.ser.read(1) == 'S')

  def manual_update(self):
    self.manual_write(chr(RGBState.CMD_UPDATE) + "\0"*3)
    assert(self.ser.read(1) == 'A')

  def manual_write(self, cmd):
    self.ser.write(cmd)

  def manual_exit(self):
    self.manual_write(RGBState.CMD_EXIT_MANUAL, [0]*3)
    val = self.ser.read(1)
    print "Val is", ord(val), val
    assert(val == 'S')

def _basic_test(con):
  con.setState(RGBState.STATE_MANUAL)
  print "State manual"
  time.sleep(4.0)
  con.manual_write(5, [255, 255, 255])
  print "Wrote color"
  time.sleep(4.0)
  con.manual_update()
  print "Updating"
  time.sleep(4.0)
  print "Exiting"
  con.manual_exit()

def _fade_test(con):
  con.setState(RGBState.STATE_MANUAL)
  for j in xrange(55):
    for i in xrange(NTOWER+NRING):
      con.manual_write(i, [j, 0, 0])  
    con.manual_update()
  for j in xrange(55, -1, -1):
    for i in xrange(NTOWER+NRING):
      con.manual_write(i, [j, 0, 0])
    con.manual_update()

  con.manual_exit()

if __name__ == "__main__":
  import serial
  import time
  
  from Inputs.USBDiscovery import get_connected_usb_devices
  usb_devices = get_connected_usb_devices()

  ser = serial.Serial(usb_devices["A9OZNP19"], 115200)
  time.sleep(3.0)

  con = RGBMultiController(ser)
  _fade_test(con)

    

    
