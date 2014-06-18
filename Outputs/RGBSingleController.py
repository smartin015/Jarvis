import struct

class RGBSingleController():

  def __init__(self, ser):
    self.ser = ser
    self.clear()

  def clear(self):
    self._writeBegin()
    self._writeColor([0, 0, 0])
    self._writeColor([0, 0, 0])

  def _writeBegin(self):
    self.ser.write(struct.pack('B', 0x01))
  
  def _writeColor(self, rgb):
    for c in rgb:
      self.ser.write(struct.pack('B', c))

  def write(self, rgb1, rgb2 = None):
    self._writeBegin()
    self._writeColor(rgb1)
    if rgb2:
      self._writeColor(rgb2)


if __name__ == "__main__":
  import serial
  import time
  ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=3)  
  time.sleep(0.5) # So arduino can initialize

  writer = RGBSingleController(ser)
    
  while True:
    sstr = raw_input("R G B: ")
    
    if not sstr or len(sstr.split(" ")) != 6:
      break

    cols = sstr.split(" ")
    c1 = [int(cols[i]) for i in xrange(3)]
    c2 = [int(cols[i+3]) for i in xrange(3)]
    writer.write(c1, c2)
     
