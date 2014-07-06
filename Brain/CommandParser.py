#!/usr/bin/env python

import time
import string
from collections import deque
import threading

import pygst
pygst.require('0.10')
import gst

from JarvisBase import JarvisBase

class CommandParser(JarvisBase):
  SILENCE_INTERVAL = 2.5 #Seconds

  def __init__(self, audiosrc, isValid, callback, trigger="jarvis", maxlength=10):
    JarvisBase.__init__(self)

    self.trigger = trigger
    self.audiosrc = audiosrc
    self.callback = callback
    self.isValid = isValid

    self.maxlen = maxlength
    self.buf = deque(maxlen = self.maxlen)

    self.last_injection = int(time.time())

    timerthread = threading.Thread(target=self.worker_thread)
    timerthread.daemon = True
    timerthread.start()

  def buffer_and_send(self, text):
    self.buf.extend(text)
    self.logger.debug(list(self.buf))
    last_injection = int(time.time())

  def extract_command(self):
    ntrigs = self.buf.count(self.trigger)

    # Pull out all words prefixing a trigger
    # And attempt to run them as a command.
    # Leaves a single trigger at the head 
    # of our buffer on failure, and removes it on success
    if ntrigs > 0:
      command_slice = []
      while self.buf[0] != self.trigger:
        command_slice.append(self.buf.popleft())
      if self.isValid(command_slice):
        self.callback(command_slice)
        assert(self.buf.popleft() == self.trigger)
        return True

    # If the above fails and there is more 
    # than one trigger in our buffer, pop the head trigger
    # so that we can run the next command
    if ntrigs > 1:
      assert(self.buf.popleft() == self.trigger)
      return True
    else:
      # Leave the trigger alone - wait until a pause before running
      return False

  def worker_thread(self):
    # Periodically check for pauses in transcription.
    # Send if a pause follows a target command,
    # Else expire if too much time elapses

    while True:
      time.sleep(0.5)

      # Try to pull out commands
      while self.extract_command():
        continue

      # If a pause occurs and a trigger is at the start of the word list, 
      # Try to run what remains as a command
      currtime = int(time.time())
      timeout = self.last_injection + DummyCommandParser.SILENCE_INTERVAL
      if currtime > timeout and len(self.buf):
        if self.buf[0] == self.trigger:
          command_slice = [self.buf.popleft() for i in xrange(len(self.buf))]
          if self.isValid(command_slice):
            self.callback(command_slice)
        else:
          # Discard old stuff
          for i in xrange(len(self.buf)):
            self.buf.popleft()

  def inject(self, text):
    self.buffer_and_send([word.strip(string.punctuation).lower() for word in text.split()])

if __name__ == "__main__":
  import gobject 
  import logging
  gobject.threads_init()
  
  def cb(s):
    print "COMMAND:", s

  cp = CommandParser(
    "test", 
    gst.element_factory_make("autoaudiosrc", "audiosrc"),
    None,
    None,
    lambda x: True,
    cb
  )

  # This loops the program until Ctrl+C is pressed
  g_loop = threading.Thread(target=gobject.MainLoop().run)
  g_loop.daemon = False
  g_loop.start()

