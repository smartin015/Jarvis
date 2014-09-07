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
#from Inputs.Kaicong.KaicongAudioGst import KaicongAudioSource
#from Inputs.Kaicong.KaicongVideo import KaicongVideo
from Inputs.TTSClient import TTSClient

from Brain.Brain import JarvisBrain
from Brain.CommandParser import CommandParser

def init_inputs(brain):
  logger.info("Initializing input devices")

  def gen_cb(room_id):
    def cb(data):
      return brain.processInput(data, room_id)
    return cb

  inputs = {}
  for i in config.TTS:
    if not inputs.get(i.room_id):
      inputs[i.room_id] = {
        "parser": CommandParser(brain.isValid, gen_cb(i.room_id)),
        "tts": []
      }

    t = TTSClient(i.id, i.host, i.port, inputs[i.room_id]['parser'].inject, brain.update_connection_status)
    t.daemon = True
    t.start()
    
    inputs[i.room_id]['tts'].append(t)
  
  # Allow custom input for keyboards
  inputs['console'] = {
    "parser": CommandParser(brain.isValid, gen_cb('console')),
  }

    
  return inputs

if __name__ == "__main__":
  brain = JarvisBrain()
  inputs = init_inputs(brain)

  logging.warn("Entering command loop")

  while True:
    #cmd = raw_input("ROOM:")
    cmd = raw_input("CMD: ")
  
    if cmd == "quit":
      logger.warn("Exiting...")
      break
    else:
      inputs['console']['parser'].inject(cmd)


