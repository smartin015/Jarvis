import logging
import serial
import time
logging.basicConfig()

from Inputs.USBDiscovery import get_connected_usb_devices
from Outputs.RFController import RFController

USB_ID = "A602KAB4"
path = get_connected_usb_devices()[USB_ID]



ser = serial.Serial(path, 9600)
con = RFController(serial.Serial("/dev/ttyUSB1", 115200), "hackspace")
while True:
  delta = target - level
  currtime = time.time()

  if delta != 0:
    level += (1 if delta > 0 else -1)
    con.send_cmd(con.CMD_FET1, level)
  
  if target == MAX_LEVEL and currtime - last_on > TIMEOUT:
    target = MIN_LEVEL

  if ser.inWaiting() > 0:
    v = ord(ser.read(1))
    print v
    if (v == 1):
      print "ON"
      last_on = time.time()
      target = MAX_LEVEL
    else:
      print "OFF"

  time.sleep(0.02)

