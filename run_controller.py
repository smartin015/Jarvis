#!/usr/bin/env python
import config
import threading
import logging
import time
import sys
from socket import gethostname
logging.basicConfig()

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

from Inputs.USBDiscovery import get_connected_usb_devices

from Outputs.RFController import RFController
from Outputs.RelayController import RelayController
from Outputs.RGBSingleController import RGBSingleController
from Outputs.RGBMultiController import RGBMultiController, RGBState
from Outputs.RunnerLightsController import RunnerLightsController
from Outputs.SpeakerController import SpeakerController
from Outputs.Controller import ControllerServer, ControllerClient
from serial import Serial

class ThreadSafeSerial(Serial):

  def __init__(self, *args, **kwargs):
    Serial.__init__(self, *args, **kwargs)
    self._writelock = threading.Lock()
    self._readlock = threading.Lock()

  def write(self, *args, **kwargs):
    self._writelock.acquire()
    rtn = Serial.write(self, *args, **kwargs)
    self._writelock.release()
    return rtn

  def read(self, *args, **kwargs):
    self._readlock.acquire()
    rtn = Serial.read(self, *args, **kwargs)
    self._readlock.release()
    return rtn

def init_outputs():
  logger.info("Initializing output devices")
  usb_devices = get_connected_usb_devices()

  # TODO: Error speech indicating if devices are missing 
  outputs = {}
  for o in config.USB:
    logger.info(o.id + " - " + o.name)
    cls = reduce(getattr, o.controller.split("."), sys.modules[__name__])
    try:
      outputs[o.name] = cls(ThreadSafeSerial(usb_devices[o.id], o.rate))
    except KeyError:
      logger.error("Could not find USB host %s (for %s)" % (o.id, o.name))
      sys.exit(-1)

  # Initialize non-USB outputs
  outputs['speaker'] = SpeakerController()

  logger.info("Outputs initialized")
  return outputs
   
if __name__ == "__main__":
  outputs = init_outputs()
  time.sleep(2.0)

  logging.warn("Starting runnerlights")
  outputs['runnerlights'].enable(outputs['RF'])

  server_address = (gethostname(), 9996)

  logging.warn("Starting control server")
  srv = ControllerServer(server_address, outputs)

  logging.warn("Entering command loop")
  cli = ControllerClient(server_address)
  while True:
    #cmd = raw_input("ROOM:")
    cmd = raw_input("CMD: ")
  
    if cmd == "quit":
      logger.warn("Exiting...")
      break
    else:
      (out, data) = cmd.split(' ', 1)
      cli.cmd(out, data)


