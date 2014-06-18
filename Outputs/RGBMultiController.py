import struct

class RGBMultiController():

  def __init__(self, ser):
    self.ser = ser
    self.clear()

  def clear(self):
    raise Exception("Unimplemented")

  def write(self, pixels):
    raise Exception("Unimpleneted")
    # Only send delta!

  def writePixel(self, rgb):
    raise Exception("Unimplemented")

  def display(self):
    raise Exception("Unimplemented")

if __name__ == "__main__":
  import serial
  import time
  ser = serial.Serial("/dev/ttyUSB1", 9600, timeout=3)  
  time.sleep(0.5) # So arduino can initialize

  writer = RGBWriter(ser)


  # TODO: Manual test
     
