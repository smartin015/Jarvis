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

from Outputs.RFController import RFController
from Outputs.RelayController import RelayController
from Outputs.RGBSingleController import RGBSingleController
from Outputs.RGBMultiController import RGBMultiController, RGBState
from Outputs.RunnerLightsController import RunnerLightsController
from Outputs.SpeakerController import SpeakerController
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
    
def init_inputs(brain, outputs):
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
  outputs = init_outputs()
  time.sleep(2.0)

  logging.warn("Starting runnerlights")
  outputs['runnerlights'].enable(outputs['RF'])

  logging.warn("Starting towerlights")

  outputs['tower'].setDefault(RGBState.STATE_FADE, keepalive=True)


  brain = JarvisBrain(outputs)
  inputs = init_inputs(brain, outputs)

  logging.warn("Entering command loop")

  while True:
    #cmd = raw_input("ROOM:")
    cmd = raw_input("CMD: ")
  
    if cmd == "quit":
      logger.warn("Exiting...")
      break
    else:
      inputs['console']['parser'].inject(cmd)


