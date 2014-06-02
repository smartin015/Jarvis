import time
import serial
import struct


text_file = open("IRCommandFiles/ProjectorPower.txt", "r")
lines = text_file.read().split(', ')
print lines
print len(lines)
text_file.close()

ser = serial.Serial('/dev/ttyUSB0', 9600)
 
time.sleep(0.5)


if ser.read(1) == "A":
     ser.write(struct.pack('>h', 32766))
     
     for x in range(0, len(lines)-1):
         ser.write(struct.pack('>h', int(float(lines[x]))))
     
     ser.write(struct.pack('>h', 32765))

print ser.readline()
