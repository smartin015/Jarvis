#!/usr/bin/env python

import threading
import logging
logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

from Tests.TestSerial import TestSerial

from Inputs.USBDiscovery import get_connected_usb_devices
from Inputs.Kaicong.KaicongAudioGst import KaicongAudioSource
from Inputs.Kaicong.KaicongVideo import KaicongVideo

from Brain.Brain import JarvisBrain
from Brain.CommandParser import CommandParser, DummyCommandParser

from serial import Serial
from Outputs.ArduinoSerial import ArduinoSerial
from Outputs.RFSerial import RFSerial

from Outputs.IRController import IRController
from Outputs.RelayController import RelayController
from Outputs.RGBSingleController import RGBSingleController
from Outputs.RGBMultiController import RGBMultiController, RGBState

# TODO: Implement these!
from Outputs.UNIMPLEMENTED.RecordingController import RecordingController
from Outputs.UNIMPLEMENTED.GMusicController import GMusicController
from Outputs.UNIMPLEMENTED.LockitronController import LockitronController
from Outputs.UNIMPLEMENTED.TimerController import TimerController
from Outputs.UNIMPLEMENTED.ScriptController import ScriptController

# Spool up output devices, create room contexts
# TODO: Do by bus ID
# TODO: Startup speech indicating which devices missing, plus new devices
logging.debug("Initializing serial devices")
LIVINGROOM_IR = TestSerial("LR")
TRACKLIGHT = Serial("/dev/ttyUSB2", 9600)
RF_BROADCAST = TestSerial("RF") 
RGBLIGHT = TestSerial("/dev/ttyACM0")#, timeout=4)
WINDOWLIGHT = Serial("/dev/ttyUSB1", 9600)
COUCHLIGHT = Serial("/dev/ttyUSB0", 9600)

MAINLIGHT = RFSerial(RF_BROADCAST, "LIVINGROOM")
HACKSPACE_IR = RFSerial(RF_BROADCAST, "HACKIR")
HACKSPACE = RFSerial(RF_BROADCAST, "HACK")
KITCHEN = RFSerial(RF_BROADCAST, "KITCHEN")
TODDROOM = RFSerial(RF_BROADCAST, "TODD")

KAICONG_LIVINGROOM = "192.168.1.19"
KAICONG_KITCHEN = "192.168.1.17"
KAICONG_HACKSPACE = "192.168.1.19"
KAICONG_TODDROOM = "192.168.1.20"

logging.debug("Initializing room contexts")

# TODO: Per-room voice
livingroom_ctx = {
  "AC": IRController(LIVINGROOM_IR),
  "projector": IRController(LIVINGROOM_IR),
  "speakers": IRController(LIVINGROOM_IR),
  "projectorscreen": IRController(LIVINGROOM_IR),
  "tracklight": RelayController(TRACKLIGHT),
  "windowlight": RGBSingleController(WINDOWLIGHT),
  "couchlight": RGBSingleController(COUCHLIGHT)
}


kitchen_ctx = {
  "mainlight": RelayController(KITCHEN),
  "speakers": RelayController(KITCHEN),
}

toddroom_ctx = {
  "mainlight": RelayController(TODDROOM),
}

hackspace_ctx = {
  "mainlight": RelayController(HACKSPACE),
  "recording": RecordingController(KAICONG_HACKSPACE),
  "AC": IRController(HACKSPACE_IR),
  "projector": IRController(HACKSPACE_IR),
}

global_ctx = {
  "music": GMusicController(),
  "lockitron": LockitronController(),
  "timer": TimerController(),
  "scripts": ScriptController(),
  "tower": RGBMultiController(RGBLIGHT, default=RGBState.STATE_FADE),
}

# Initialize the brain
brain = JarvisBrain()

logger.info("Spooling up audio pipelines")
import gobject 
gobject.threads_init()

import pygst
pygst.require('0.10')
import gst

gobject.type_register(KaicongAudioSource)
gst.element_register(KaicongAudioSource, 'kaicongaudiosrc', gst.RANK_MARGINAL)

def gen_kaicong_audio_src(ip):
  src = gst.element_factory_make("kaicongaudiosrc", "audiosrc")
  src.set_property("ip", ip)
  src.set_property("user", "jarvis_admin")
  src.set_property("pwd", "oakdale43")
  src.set_property("on", True)
  return src

def gen_microphone_src(device_number):
  src = gst.element_factory_make("pulsesrc", "src")
  src.set_property("device", device_number)
  return src

def gen_auto_src(*args, **kwargs):
  src = gst.element_factory_make("autoaudiosrc", "audiosrc")
  return src

# Initialize input devices and attach callbacks (with contexts)
def gen_callback(ctx):
  joined_ctx = dict(global_ctx.items() + ctx.items())
  def cb(input):
    return brain.processInput(joined_ctx, input)
  return cb

# Here's where you edit the vocabulary.
# Point these variables to your *.lm and *.dic files. A default exists, 
# but new models can be created for better accuracy. See instructions at:
# http://cmusphinx.sourceforge.net/wiki/tutoriallm
LM_PATH = '/home/jarvis/Jarvis/Brain/commands.lm'
DICT_PATH = '/home/jarvis/Jarvis/Brain/commands.dic'

livingroom_cb = gen_callback(livingroom_ctx)

audio_sources = {
  "livingroom": CommandParser("lr",
    gen_microphone_src(3), 
    LM_PATH, DICT_PATH, brain.isValid, livingroom_cb
  ), 
  "livingroom_desks": CommandParser("lrd",
    gen_microphone_src(5),
    LM_PATH, DICT_PATH, brain.isValid, livingroom_cb
  ),
#  "kitchen": SpeechParser(
#    gen_kaicong_audio_src(KAICONG_KITCHEN), gen_callback(kitchen_ctx)
#  ),
#  "hackspace": SpeechParser(
#    gen_kaicong_audio_src(KAICONG_HACKSPACE), gen_callback(hackspace_ctx)
#  ),
#  "toddroom": SpeechParser(
#    gen_kaicong_audio_src(KAICONG_TODDROOM), gen_callback(toodroom_ctx)
#  ),
}

# Loop the gstreamer pipeline in the background
logger.info("Starting main audio thread")
g_loop = threading.Thread(target=gobject.MainLoop().run)
g_loop.daemon = True
g_loop.start()

# TODO: Setup and run CV stuff as well
while True:
  #cmd = raw_input("ROOM:")
  cmd = raw_input("CMD: ")

  if cmd == "quit":
    print "Exiting..."
    break
  else:
    audio_sources['livingroom'].inject(cmd)


