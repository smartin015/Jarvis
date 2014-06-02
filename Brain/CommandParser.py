#!/usr/bin/env python

import time
import string
from collections import deque

import pygst
pygst.require('0.10')
import gst


from JarvisBase import JarvisBase

class DummyCommandParser(JarvisBase):
  CLEAR_INTERVAL = 3

  def __init__(self, audiosrc, callback, trigger="jarvis", maxlength=10):
    JarvisBase.__init__(self)

    self.trigger = trigger
    self.audiosrc = audiosrc
    self.callback = callback

    self.maxlen = maxlength
    self.wordbuffer = deque(maxlen = self.maxlen)

    self.active_listen_mode = False

    self.last_injection = int(time.time())

  def send(self):
    """ Triggers sending a command - whatever's in the word buffer """
    command_slice = list(self.wordbuffer)
    self.wordbuffer.clear()
    self.logger.info("Sending command: %s" % (" ".join(command_slice)))
    result = self.callback(command_slice)

  def buffer_and_send(self, text):
    # Automatically timeout old words
    currtime = int(time.time())
    if currtime > (self.last_injection + DummyCommandParser.CLEAR_INTERVAL):
      self.send()
    self.last_injection = currtime

    self.wordbuffer.extend(text)
    self.logger.debug(list(self.wordbuffer))

    # Commands only ever valid if the trigger is at the very start or end,
    # Thus we basically have a CSV of commands by trigger value separator
    while self.trigger in list(self.wordbuffer):
      # See if the command evaluates with the trigger as an ending word
      trigger_idx = list(self.wordbuffer).index(self.trigger)
      command_slice = [self.wordbuffer.popleft() for _i in xrange(trigger_idx)]
      self.wordbuffer.popleft() # Pop the trigger
      self.logger.info("Sending command: %s" % (" ".join(command_slice)))
      result = self.callback(command_slice)
    
  def inject(self, text):
    self.buffer_and_send([word.strip(string.punctuation).lower() for word in text.split()])

class CommandParser(DummyCommandParser):
  # Here's where you edit the vocabulary.
  # Point these variables to your *.lm and *.dic files. A default exists, 
  # but new models can be created for better accuracy. See instructions at:
  # http://cmusphinx.sourceforge.net/wiki/tutoriallm
  LM_PATH = '/home/jarvis/Jarvis/Brain/9812.lm'
  DICT_PATH = '/home/jarvis/Jarvis/Brain/9812.dic'

  def __init__(self, audiosrc, callback):
    DummyCommandParser.__init__(self, audiosrc, callback)
    
    self.logger.info("Creating audio pipeline")
    pipeline = gst.Pipeline()
    
    self.heartbeat_count = 0
    audiosrc.connect('packet_received', self.heartbeat)

    conv = gst.element_factory_make("audioconvert", "audioconv")
    res = gst.element_factory_make("audioresample", "audioresamp")
    
    vader = gst.element_factory_make("vader", "vad")
    vader.set_property("auto-threshold", True)
    
    asr = gst.element_factory_make("pocketsphinx", "asr")
    asr.connect('partial_result', self.asr_partial_result)
    asr.connect('result', self.asr_result)
    
    # Set the language model and dictionary.
    asr.set_property('lm', CommandParser.LM_PATH)
    asr.set_property('dict', CommandParser.DICT_PATH)

    # Now tell gstreamer and pocketsphinx to start converting speech!
    asr.set_property('configured', True)
    
    sink = gst.element_factory_make("fakesink", "fs")
    
    pipeline.add(audiosrc, conv, res, vader, asr, sink)
    gst.element_link_many(audiosrc, conv, res, vader, asr, sink)
    pipeline.set_state(gst.STATE_PLAYING)
    
  def heartbeat(self, asrc):
    # Send if enough of a pause elapses
    self.heartbeat_count += 1
    if self.heartbeat_count > 15:
      self.heartbeat_count = 0
      self.send()

  def asr_partial_result(self, asr, text, uttid):
    """ This function is called when pocketsphinx gets a partial
        transcription of spoken audio. 
    """
    self.heartbeat_count = 0
    #self.logger.debug("%sP: %s" % (uttid, text))
    
  def asr_result(self, asr, text, uttid):
    """ This function is called when pocketsphinx gets a 
        full result (spoken command with a pause)
    """

    self.logger.debug(text)
    self.inject(text)
    
if __name__ == "__main__":
  import gobject 
  gobject.threads_init()

  # This loops the program until Ctrl+C is pressed
  g_loop = threading.Thread(target=GObject.MainLoop().run)
  g_loop.daemon = False
  g_loop.start()
