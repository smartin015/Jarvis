#!/usr/bin/env python
import gi
gi.require_version('Gst', '0.10')
from gi.repository import GObject, Gst
import threading

print Gst.version()

# Here's where you edit the vocabulary.
# Point these variables to your *.lm and *.dic files. A default exists, 
# but new models can be created for better accuracy. See instructions at:
# http://cmusphinx.sourceforge.net/wiki/tutoriallm
LM_PATH = '9812.lm'
DICT_PATH = '9812.dic'

# Initialize GST
GObject.threads_init()
Gst.init(None)

def asr_partial_result(asr, text, uttid):
    """ This function is called when pocketsphinx gets a partial
        transcription of spoken audio. 
    """
    print "ASR partial", uttid, ":", text

def asr_result(asr, text, uttid):
    """ This function is called when pocketsphinx gets a 
        full result (spoken command with a pause)
    """
    print "ASR result", uttid, ":", text

# This sets up our pipeline from pulseaudio (input) 
# through the vader and into pocketsphinx.
pipeline = Gst.parse_launch('pulsesrc ! audioconvert ! audioresample '
                             + '! vader name=vad auto-threshold=true '
                             + '! pocketsphinx name=asr ! fakesink')

# Connect our callbacks to pocketsphinx
asr = pipeline.get_by_name('asr')
asr.connect('partial_result', asr_partial_result)
asr.connect('result', asr_result)

# Optional: set the language model and dictionary.
if LM_PATH and DICT_PATH:
  asr.set_property('lm', LM_PATH)
  asr.set_property('dict', DICT_PATH)

# Now tell gstreamer and pocketsphinx to start converting speech!
asr.set_property('configured', True)
pipeline.set_state(Gst.State.PLAYING)

# This loops the program until Ctrl+C is pressed
g_loop = threading.Thread(target=GObject.MainLoop().run)
g_loop.daemon = False
g_loop.start()
