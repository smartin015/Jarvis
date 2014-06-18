import time
from RGBWriter import RGBWriter
import serial
import random
  
ser = serial.Serial('/dev/ttyUSB1', 9600)
writer = RGBWriter(ser)

ser2 = serial.Serial('/dev/ttyUSB0', 9600)
writer2 = RGBWriter(ser2)
time.sleep(0.1)

def blinky():
  cols = [random.randint(0, 255) for i in xrange(3)]
  cols2 = [random.randint(0, 255) for i in xrange(3)]
  writer.write(cols, cols2)

  cols3 = [random.randint(0, 255) for i in xrange(3)]
  writer2.write(cols3)

while True:
  blinky()
  time.sleep(0.1)
