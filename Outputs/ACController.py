import time
import serial
import struct
import sys

ser = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(2.5)

print "Clap on"
ser.write('T')
print ser.read(1)

time.sleep(2.0)

print "Clap off"
ser.write('F')
print ser.read(1)



