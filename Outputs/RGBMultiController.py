import time

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

  def manual_update(self):
    self.ser.write(chr(RGBState.CMD_UPDATE)*4)

  def manual_write(self, i, rgb):
    rgb = [chr(c) for c in rgb]
    self.ser.write(chr(i) + "".join(rgb))

  def manual_exit(self):
    self.ser.write(chr(RGBState.CMD_EXIT_MANUAL)*4)

if __name__ == "__main__":
  import serial
  import time
  ser = serial.Serial("/dev/ttyACM0", 115200)
  time.sleep(1.5)

  con = RGBMultiController(ser)

  #while True:
  #  sstr = raw_input("State: ")
  #  con.setState(int(sstr))


  con.setState(RGBState.STATE_MANUAL)
  print "set manual"
  time.sleep(2.0)
  con.manual_write(5, [255, 0, 0])
  con.manual_update()
  print "wrote R"
  time.sleep(2.0)
  con.manual_write(5, [0, 255, 0])
  con.manual_update()
  print "wrote G"
  time.sleep(2.0)

  con.manual_exit()
    

    
