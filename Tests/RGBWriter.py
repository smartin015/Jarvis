import time
import struct

def writeBegin():
  ser.write(chr(0x01))

def writeColor(rgb):
  for c in rgb:
    ser.write(struct.pack('B', c))

def writeGradient():
  for i in xrange(0,256, 1):
    writeBegin()
    writeColor([i, i, i])
    writeColor([i, i, i])
  for i in xrange(255,-1, -1):
    writeBegin()
    writeColor([i, i, i])
    writeColor([i, i, i])



if __name__ == "__main__":
  import serial
  ser = serial.Serial("/dev/ttyUSB1", 9600, timeout=3)  
  time.sleep(0.5)
  print "Connected... reading"

  writeBegin()
  writeColor([0, 0, 0])
  writeColor([0, 0, 0])

  while True:
    sstr = raw_input("R G B: ")
    
    if not sstr or len(sstr.split(" ")) != 6:
      break

    cols = sstr.split(" ")
    c1 = [int(cols[i]) for i in xrange(3)]
    c2 = [int(cols[i+3]) for i in xrange(3)]
    writeBegin()
    writeColor(c1)
    writeColor(c2)
     

  while True:
    writeGradient()



  while True:
    writeBegin()
    writeColor([80, 20, 0])
    writeColor([128, 20, 0])
    time.sleep(0.1)
  
  while True:
    writeBegin()
    writeColor([0, 255, 0])
    time.sleep(0.5)
    writeColor([0, 255, 0])
    time.sleep(0.5)
    writeBegin()
    writeColor([255, 0, 0])
    time.sleep(0.5)
    writeColor([255, 0, 0])
    time.sleep(0.5)
    writeBegin()
    writeColor([0, 0, 255])
    time.sleep(0.5)
    writeColor([0, 0, 255])
    time.sleep(0.5)


