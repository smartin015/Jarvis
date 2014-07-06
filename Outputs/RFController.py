import time
import serial
import struct
import logging
from Controller import Controller

class RFController(Controller):
  CMD_FET1 = 0x00
  CMD_FET2 = 0x01
  CMD_RELAY = 0x02
  CMD_IR_BUFFER = 0x10
  CMD_IR_SEND = 0x11
  CMD_IR_RESET = 0x12
  CMD_IR_TEST = 0x14

  def __init__(self, ser, ir_path = "Outputs/IRCommandFiles/"):
    Controller.__init__(self)
    self.ser = ser
    self.ir_path = ir_path
    self.logger.setLevel(logging.INFO)

  def send_cmd(self, cmd, val):
    if val == "ON":
      val = 0x01
    elif val == "OFF":
      val = 0x00
    
    self.logger.debug("Sending " + str(cmd) + str(val))
    self.ser.write(chr(cmd));
    self.ser.write(struct.pack('>h', int(val)));

    v = self.ser.readline()
    while v.strip() != "":
      self.logger.warn(v)
      v = self.ser.readline()

  def send_IR(self, fil):
    with open(self.ir_path + fil, 'r') as f:
      data = f.read()
    data = [d.strip() for d in data.split(",")]

    self.send_cmd(self.CMD_IR_RESET, 0)
    for b in data:
      self.send_cmd(self.CMD_IR_BUFFER, int(b))

    self.send_cmd(self.CMD_IR_SEND, 3)

    self.logger.info("IR written")
    time.sleep(0.5)

if __name__ == "__main__":
  import logging
  logging.basicConfig()
  ser = serial.Serial("/dev/ttyUSB1", 115200)
  con = RFController(ser)

  while True:
    cmdstr = raw_input("CMD (RELAY/FET1/2 ON/OFF, IR <file>):")
    if len(cmdstr.split()) == 1:
      if cmdstr == "SCDN":
        con.send_IR("ProjectorScreenDown.txt")
      elif cmdstr == "SCST":
        con.send_IR("ProjectorScreenStop.txt")
      elif cmdstr == "SCUP":
        con.send_IR("ProjectorScreenUp.txt")
      elif cmdstr == "IRTEST":
        con.send_cmd(con.CMD_IR_TEST, val)
      continue
      

    (cmd, val) = cmdstr.split()

    if cmd == "RELAY":
      con.send_cmd(con.CMD_RELAY, val)
    elif cmd == "FET1":
      con.send_cmd(con.CMD_FET1, val)
    elif cmd == "FET2":
      con.send_cmd(con.CMD_FET2, val)
    elif cmd == "IR":
      con.send_IR(val)

      
