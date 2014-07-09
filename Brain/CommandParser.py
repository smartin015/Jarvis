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
  SILENCE_INTERVAL = 1.5 #Seconds
  PARTIAL_APPEND_INTERVAL = 0.5 #Seconds

  def __init__(self, isValid, callback, trigger="jarvis", maxlength=10):
    JarvisBase.__init__(self)

    self.trigger = trigger.lower()
    self.callback = callback
    self.isValid = isValid

    self.maxlen = maxlength

    # Stores full transcription (or timed-out partial transcription) data
    # for eventual processing by the worker thread
    self.buf = deque(maxlen = self.maxlen)

    # Stores unbuffered partial transcription data
    self.partial = []

    # The current transcription uttid
    self.uttid = None

    # For partial transcription, the number of words we've already buffered
    self.cutoff = 0  

    # The time of last injection. If longer than SILENCE_INTERVAL ago, 

    self.last_injection = int(time.time())

    t = threading.Thread(target=self.worker_thread)
    t.daemon = True
    t.start()

  def add_to_buffer(self, word_list, uttid = None):
    last_injection = int(time.time())

    if uttid is None:
      self.buf.extend(word_list)
      self.logger.debug("BUF: " + str(list(self.buf)))
    else:
      if uttid != self.uttid:
        self.dump_partial_to_buffer()
        self.cutoff = 0
        self.uttid = uttid

      self.partial = word_list[(self.cutoff):]
      self.logger.debug("PAR: " + str(list(self.partial)))


  def extract_command(self):
    ntrigs = self.buf.count(self.trigger)
    consumed = False

    # If we're starting on a trigger, consume it 
    # and everything up to the next trigger, leaving   
    # the next one in the buffer
    if ntrigs > 1 and self.buf[0] == self.trigger:
      assert(self.buf.popleft() == self.trigger)
      consumed = True
    
    # Pull out all words prefixing a trigger
    # And attempt to run them as a command.
    if ntrigs > 0:
      command_slice = []
      while self.buf[0] != self.trigger:
        command_slice.append(self.buf.popleft())
      #print "Extracted", command_slice
      if len(command_slice) and self.isValid(command_slice):
        self.callback(command_slice)

        # If we found a command prefixing a trigger and didn't
        # already consume one, pop the one at the buffer head
        if not consumed:
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

  def dump_partial_to_buffer(self):
    partial_len = len(self.partial)
    self.buf.extend(self.partial)
    self.cutoff += partial_len
    self.partial = []
    if partial_len:
      self.logger.debug("BUF: " + str(list(self.buf)))


  def worker_thread(self):
    # Periodically check for pauses in transcription.
    # Send if a pause follows a target command,
    # Else expire if too much time elapses

    while True:
      time.sleep(0.5)
      currtime = int(time.time())

      # Append partial transcriptions if expired
      if currtime > self.last_injection + self.PARTIAL_APPEND_INTERVAL: 
        self.dump_partial_to_buffer()

      # Try to pull out commands
      while self.extract_command():
        continue

      # If a pause occurs and a trigger is at the start of the word list, 
      # Try to run what remains as a command
      if currtime > self.last_injection + self.SILENCE_INTERVAL and len(self.buf):
        #print "Silence, have:", list(self.buf)
        if self.buf[0] == self.trigger:
          command_slice = [self.buf.popleft() for i in xrange(len(self.buf))]
          command_slice = [c for c in command_slice if c != self.trigger]        
          if self.isValid(command_slice):
            self.callback(command_slice)
        else:
          # Discard old stuff
          #print "Discarding", list(self.buf)
          for i in xrange(len(self.buf)):
            self.buf.popleft()

  def inject(self, text, uttid = None):
    self.add_to_buffer([word.strip(string.punctuation).lower() for word in text.split()], uttid)

if __name__ == "__main__":
  import logging
  logging.basicConfig()

  def gen_cb(expected, evt):
    
    def cb(s):
      print "COMMAND:", s
      e = expected.pop(0)
      if (s != e):
        raise Exception("Got %s but expected %s" % (s, e))

      if len(expected) == 0:
        evt.set()

    return cb

  def test(parser, words, *args):
    parser.callback = gen_cb(list(args), cp.evt)
    parser.inject(words)
    cp.evt.wait()
    cp.evt.clear()

  def uttid_test(parser, *args, **kwargs):
    parser.callback = gen_cb(kwargs['results'], cp.evt)
    for (uttid, text) in args:
      parser.inject(text, uttid)
    cp.evt.wait()
    cp.evt.clear()

  cp = CommandParser(
    lambda x: True,
    None
  )
  cp.evt = threading.Event()

  # Test basic injection and ordering
  
  test(cp, "projector jarvis", ['projector'])
  test(cp, "jarvis projector", ['projector'])
  test(cp, "herp de derp jarvis", ['herp', 'de', 'derp'])
  test(cp, "projector jarvis lights jarvis", ['projector'], ['lights'])
  test(cp, "jarvis projector jarvis lights", ['projector'], ['lights'])
  test(cp, "projector jarvis jarvis lights", ['projector'], ['lights'])
  

  # Test injection with uttid
  uttid_test(cp, (1, "jarvis projector"), (1, "jarvis lights"), results=[['lights']])
  uttid_test(cp, (2, "jarvis"), (3, "projector"), results=[['projector']])
  uttid_test(cp, (3, "projector jarvis lights"), results=[['lights']])
  uttid_test(cp, (3, "projector jarvis lights audio jarvis"), results=[['audio']])
  uttid_test(cp, (4, "jarvis"), (5, "jarvis"), (6, "jarvis"), (7, "lights"), results=[['lights']])

