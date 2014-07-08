

import serial
import time

ser = serial.Serial("/dev/ttyUSB4", 9600)
time.sleep(2.0)

while True:
  print "Turning on"
  ser.write('T')
  
  time.sleep(1.0)
  
  print "Turning off"
  ser.write('F')

  time.sleep(1.0)
