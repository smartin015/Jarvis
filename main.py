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
  for room in config.OUTPUTS:
    outputs[room] = {}
    for name in config.OUTPUTS[room]:
      (cls, usb_id, baud) = config.OUTPUTS[room][name]
      cls = reduce(getattr, cls.split("."), sys.modules[__name__])
      outputs[room][name] = cls(Serial(usb_devices[usb_id], baud))

  logger.info("Outputs initialized")
  return outputs
    
def init_inputs(brain, outputs):
  logger.info("Initializing input devices")

  def cb(data):
    return brain.processInput(outputs, data)

  inputs = {}
  for name in config.INPUTS:
    parser = CommandParser(brain.isValid, cb)
    tts = []
    for tts_name in config.INPUTS[name]['tts']:
      host = config.TTS[tts_name]['host']
      port = config.TTS[tts_name]['port']
      t = TTSClient(tts_name, host, port, parser.inject)
      t.daemon = True
      t.start()
      tts.append(t)

    # TODO: eventually we'll have CV here

    inputs[name] = {"parser": parser, "tts": tts}
  return inputs

if __name__ == "__main__":
  outputs = init_outputs()
  brain = JarvisBrain()
  inputs = init_inputs(brain, outputs)

  time.sleep(0.2)

  while True:
    #cmd = raw_input("ROOM:")
    cmd = raw_input("CMD: ")
  
    if cmd == "quit":
      logger.warn("Exiting...")
      break
    else:
      inputs['livingroom']['parser'].inject(cmd)


