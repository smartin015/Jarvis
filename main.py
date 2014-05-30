from brain.Brain import JarvisBrain

import serial
from Outputs.RFSerial import RFSerial

from Outputs.IRController import IRController
from Outputs.SwitchController import SwitchController
from Outputs.RelayController import RelayController
from Outputs.FMController import FMController

from Outputs.RecordingController import RecordingController
from Outputs.GMusicController import GMusicController
from Outputs.LockitronController import LockitronController
from Outputs.TimerController import TimerController
from Outputs.ScriptController import ScriptController

from Inputs.SphinxSTT import SphinxSTT
from Inputs.KaicongAudioGst import KaicongAudioSource

# Spool up output devices, create room contexts
LIVINGROOM_IR = serial.Serial("COM2", 9600)
TRACKLIGHT = serial.Serial("COM4", 9600)
RF_BROADCAST = serial.Serial("COM1", 9600)


MAINLIGHT = RFSerial(RF_BROADCAST, "LIVINGROOM")
HACKSPACE_IR = RFSerial(RF_BROADCAST, "HACKIR")
HACKSPACE = RFSerial(RF_BROADCAST, "HACK")
KITCHEN = RFSerial(RF_BROADCAST, "KITCHEN")
TODDROOM = RFSerial(RF_BROADCAST, "TODD")

livingroom_ctx = {
  "AC": IRController(LIVINGROOM_IR, "AC.ir"),
  "projector": IRController(LIVINGROOM_IR, "projector.ir"),
  "speakers": IRController(LIVINGROOM_IR, "speakers.ir"),
  "projectorscreen": IRController(LIVINGROOM_IR, "projectorscreen.ir"),
  "mainlight": SwitchController(MAINLIGHT),
  "tracklight": RelayController(TRACKLIGHT),
}

kitchen_ctx = {
  "mainlight": SwitchController(KITCHEN),
  "speakers": FMController(KITCHEN),
}

toddroom_ctx = {
  "mainlight": RelayController(TODDROOM),
}

hackspace_ctx = {
  "mainlight": SwitchController(HACKSPACE),
  "recording": RecordingController(),
  "AC": IRController(HACKSPACE_IR, "AC.ir"),
  "projector": IRController(HACKSPACE_IR, "projector_optoma.ir"),
}

global_ctx = {
  "music": GMusicController(),
  "lockitron": LockitronController(),
  "timer": TimerController(),
  "scripts": ScriptController(),
}

# Initialize the brain
brain = JarvisBrain()

# Initialize input devices and attach callbacks (with contexts)
KAICONG_LIVINGROOM = "192.168.1.15"
KAICONG_KITCHEN = "192.168.1.17"
KAICONG_HACKSPACE = "192.168.1.19"
KAICONG_TODDROOM = "192.168.1.20"

def gen_callback(ctx):
  joined_ctx = dict(global_ctx.items(), ctx.items())
  def cb(input):
    brain.processInput(joined_ctx, input)
  return cb


# TODO: We're probably going to have to figure out how to run 
# multiple gstreamer streams within a single 
audio_sources = [
  SphinxSTT(KaicongAudioSource(KAICONG_LIVINGROOM), gen_callback(livingroom_ctx)),
  SphinxSTT(KaicongAudioSource(KAICONG_KITCHEN), gen_callback(kitchen_ctx)),
  SphinxSTT(KaicongAudioSource(KAICONG_HACKSPACE), gen_callback(hackspace_ctx)),
  SphinxSTT(KaicongAudioSource(KAICONG_TODDROOM), gen_callback(toodroom_ctx)),
]

# Begin audio recording and transcription
for src in audio_sources:
  src.run()


# TODO: Setup and run CV stuff as well
