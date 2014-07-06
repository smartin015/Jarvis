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
  from Inputs.USBDiscovery import get_connected_usb_devices

  usb_devices = get_connected_usb_devices()
  
  sstr = raw_input("1 for couch, 2 for window")
  if sstr == "2":
    count = 6
    path = usb_devices["A9MX5JNZ"]
  elif sstr == "1":
    path = usb_devices["A70257T7"]
    count = 3

  ser = serial.Serial(path, 9600, timeout=3)  
  time.sleep(0.5) # So arduino can initialize
  writer = RGBSingleController(ser)

  while True:
    sstr = raw_input("RGB: ")
    
    if not sstr or len(sstr.split(" ")) != count:
      break

    cols = sstr.split(" ")
    if count > 3:
      c2 = [int(cols[i+3]) for i in xrange(3)]
      c1 = [int(cols[i]) for i in xrange(3)]
    else:
      c1 = [int(cols[i]) for i in xrange(3)]
      c2 = c1
    writer.write(c1, c2)

     
