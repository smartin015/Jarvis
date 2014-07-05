import time
import serial
import struct

CMD_FET1 = 0x00
CMD_FET2 = 0x01
CMD_RELAY = 0x02
CMD_IR_BUFFER = 0x10
CMD_IR_SEND = 0x11
CMD_IR_RESET = 0x12
CMD_IR_TEST = 0x14

def send_cmd(cmd, val):
  if val == "ON":
    val = 0x01
  elif val == "OFF":
    val = 0x00
  
  print "Sending", cmd, val
  ser.write(chr(cmd));
  ser.write(struct.pack('>h', int(val)));

  v = ser.readline()
  while v.strip() != "":
    print v
    v = ser.readline()

def send_IR(fil):
  with open("../../IRCommandFiles/" + fil, 'r') as f:
    data = f.read()
  data = [d.strip() for d in data.split(",")]

  send_cmd(CMD_IR_RESET, 0)
  for b in data:
    send_cmd(CMD_IR_BUFFER, int(b))

  send_cmd(CMD_IR_SEND, 3)

  print "IR written"

ser = serial.Serial("/dev/ttyUSB1", 115200)
print ser.readline()

while True:
  cmdstr = raw_input("CMD (RELAY/FET1/2 ON/OFF, IR <file>):")
  if len(cmdstr.split()) == 1:
    if cmdstr == "SCDN":
      send_IR("ProjectorScreenDown.txt")
    elif cmdstr == "SCST":
      send_IR("ProjectorScreenStop.txt")
    elif cmdstr == "SCUP":
      send_IR("ProjectorScreenUp.txt")
    elif cmdstr == "IRTEST":
      send_cmd(CMD_IR_TEST, val)
    continue
    

  (cmd, val) = cmdstr.split()

  if cmd == "RELAY":
    send_cmd(CMD_RELAY, val)
  elif cmd == "FET1":
    send_cmd(CMD_FET1, val)
  elif cmd == "FET2":
    send_cmd(CMD_FET2, val)
  elif cmd == "IR":
    send_IR(val)

    
