#!/usr/bin/env python

import pygst
pygst.require('0.10')
import gst

from JarvisBase import JarvisBase

class SpeechParser(JarvisBase):
  # Here's where you edit the vocabulary.
  # Point these variables to your *.lm and *.dic files. A default exists, 
  # but new models can be created for better accuracy. See instructions at:
  # http://cmusphinx.sourceforge.net/wiki/tutoriallm
  LM_PATH = '/home/semartin/Documents/gstreamer_pocketsphinx_demo/9812.lm'
  DICT_PATH = '/home/semartin/Documents/gstreamer_pocketsphinx_demo/9812.dic'

  def __init__(self, audiosrc, callback):
    JarvisBase.__init__(self)
    
    self.audiosrc = audiosrc
    self.callback = callback
    
    # TODO: Make pipeline
    pipeline = gst.Pipeline()
    
    conv = gst.element_factory_make("audioconvert", "audioconv")
    res = gst.element_factory_make("audioresample", "audioresamp")
    
    vader = gst.element_factory_make("vader", "vad")
    vader.set_property("auto-threshold", True)
    
    asr = gst.element_factory_make("pocketsphinx", "asr")
    asr.connect('partial_result', asr_partial_result)
    asr.connect('result', asr_result)
    
    # Set the language model and dictionary.
    asr.set_property('lm', SpeechParser.LM_PATH)
    asr.set_property('dict', SpeechParser.DICT_PATH)

    # Now tell gstreamer and pocketsphinx to start converting speech!
    asr.set_property('configured', True)
    
    sink = gst.element_factory_make("fakesink", "fs")
    
    pipeline.add(audiosrc, conv, res, vader, asr, sink)
    gst.element_link_many(audiosrc, conv, res, vader, asr, sink)
    pipeline.set_state(gst.STATE_PLAYING)
    
  def asr_partial_result(self, text, uttid):
    """ This function is called when pocketsphinx gets a partial
        transcription of spoken audio. 
    """
    self.logger.debug("%sP: %s" % (uttid, text))
    
  def asr_result(self, text, uttid):
    """ This function is called when pocketsphinx gets a 
        full result (spoken command with a pause)
    """
    self.logger.debug(text)
    self.inject(text)
    
  def inject(self, text):
    self.callback([word.strip(string.punctuation) for word in text.split()])

if __name__ == "__main__":
  import gobject 
  gobject.threads_init()

  # This loops the program until Ctrl+C is pressed
  g_loop = threading.Thread(target=GObject.MainLoop().run)
  g_loop.daemon = False
  g_loop.start()
