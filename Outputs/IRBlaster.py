import time
import serial
import struct
import sys


text_file = open("IRCommandFiles/ProjectorPower.txt", "r")
lines = text_file.read().split(', ')
text_file.close()

ser = serial.Serial('/dev/ttyUSB0', 9600)
r = ser.read(1)
print r
assert (r == 'X')
time.sleep(0.5)

START = 32766
END = 32765

lines = [START] + lines + [END]

for x in lines:
   val = int(float(x))
   ser.write(struct.pack('<h', val))
   resp = struct.unpack('<h', ser.read(2))[0]
   assert(val == resp)

ser.flush()

print "Data sent, reading..."

while True:
  sys.stdout.write(ser.read(1))

