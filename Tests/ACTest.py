

import serial
import time

ser = serial.Serial("/dev/ttyUSB3", 9600)


while True:
  print "Turning on"
  ser.write('T')
  
  time.sleep(1.0)
  
  print "Turning off"
  ser.write('F')

  time.sleep(1.0)
