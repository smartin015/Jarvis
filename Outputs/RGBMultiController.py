import time

NLIGHTS = 105
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
  STATE_MANUAL = 9

  CMD_UPDATE = 0xff
  CMD_EXIT_MANUAL = 0xfe

class RGBMultiController():
  def __init__(self, ser, default = None):
    self.ser = ser
    self.default = default

  def __del__(self):
    self.ser.close()

  def setDefault(self, state):
    self.default = state

  def setState(self, state):
    self.ser.write(chr(state))
    time.sleep(0.015)

  def manual_update(self):
    self.manual_write(RGBState.CMD_UPDATE, [0]*3)
    # Delay determined empirically. 
    # This is the lowest we could get before inconsistencies showed up
    time.sleep(0.0095) 

  def manual_write(self, i, rgb):
    cmd = chr(i) + "".join([chr(c) for c in rgb])
    self.ser.write(cmd)

  def manual_exit(self):
    self.manual_write(RGBState.CMD_EXIT_MANUAL, [0]*3)

if __name__ == "__main__":
  import serial
  import time
  ser = serial.Serial("/dev/ttyACM0", 115200)
  time.sleep(3.0)

  con = RGBMultiController(ser)
  con.setState(RGBState.STATE_MANUAL)
  for j in xrange(55):
    for i in xrange(NLIGHTS+NRING):
      con.manual_write(i, [j, 0, 0])  
    con.manual_update()
  for j in xrange(55, -1, -1):
    for i in xrange(NLIGHTS+NRING):
      con.manual_write(i, [j, 0, 0])
    con.manual_update()

  con.manual_exit()
    

    
