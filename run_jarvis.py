#!/usr/bin/env python
import config
import threading
import logging
import time
import sys
logging.basicConfig()

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

from Tests.TestSerial import TestSerial

from Inputs.USBDiscovery import get_connected_usb_devices
from Inputs.Kaicong.KaicongAudioGst import KaicongAudioSource
from Inputs.Kaicong.KaicongVideo import KaicongVideo
from Inputs.TTSClient import TTSClient

from Brain.Brain import JarvisBrain
from Brain.CommandParser import CommandParser

from Outputs.RFController import RFController
from Outputs.RelayController import RelayController
from Outputs.RGBSingleController import RGBSingleController
from Outputs.RGBMultiController import RGBMultiController, RGBState
from serial import Serial

def init_outputs():
  logger.info("Initializing output devices")
  usb_devices = get_connected_usb_devices()

  # TODO: Error speech indicating if devices are missing 
  outputs = {}
  for o in config.OUTPUTS:
    cls = reduce(getattr, o.controller.split("."), sys.modules[__name__])
    outputs[o.name] = cls(Serial(usb_devices[o.id], o.rate))

  logger.info("Outputs initialized")
  return outputs
    
def init_inputs(brain, outputs):
  logger.info("Initializing input devices")

  def cb(data):
    return brain.processInput(outputs, data)

  inputs = {}
  for i in config.TTS:
    if not inputs.get(i.room_id):
      inputs[i.room_id] = {
        "parser": CommandParser(brain.isValid, cb),
        "tts": []
      }

    t = TTSClient(i.id, i.host, i.port, inputs[i.room_id]['parser'].inject)
    t.daemon = True
    t.start()
    
    inputs[i.room_id]['tts'].append(t)
    
  return inputs

if __name__ == "__main__":
  outputs = init_outputs()
  brain = JarvisBrain()
  inputs = init_inputs(brain, outputs)
  time.sleep(2.0)
  print "Starting towerlights"

  outputs['tower'].setDefault(RGBState.STATE_FADE)
  outputs['tower'].defaultState()

  raw_input("Enter to continue")

  while True:
    #cmd = raw_input("ROOM:")
    cmd = raw_input("CMD: ")
  
    if cmd == "quit":
      logger.warn("Exiting...")
      break
    else:
      inputs['livingroom']['parser'].inject(cmd)


