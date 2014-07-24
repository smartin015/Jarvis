#!/usr/bin/env python

import time
import string
from collections import deque
import Queue
import threading

import pygst
pygst.require('0.10')
import gst

from JarvisBase import JarvisBase

class CommandParser(JarvisBase):
  INJECTION_DELAY = 0.1
  SPEECH_TIMEOUT = 0.5

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

    self.inj_queue = Queue.Queue()

    t = threading.Thread(target=self.worker_thread)
    t.daemon = True
    t.start()

  def worker_thread(self):
    while True:
      try:
        (words, uttid) = self.inj_queue.get(timeout = self.SPEECH_TIMEOUT)
      except Queue.Empty:
        self.clear_buffer()
        continue

      # Wait just a little bit to ensure no other incoming transcriptions
      # with the same UTTID (i.e. better transcriptions).
      time.sleep(self.INJECTION_DELAY)
      if not self.inj_queue.empty() and self.inj_queue.queue[0][1] == uttid:
        continue # Discard this transcription in favor of the new one

      self.buffer_and_send(words, uttid)

  def clear_buffer(self):
    self.buf.clear()
    self.cutoff = len(self.partial)

  def buffer_and_send(self, word_list, uttid = None):
    last_injection = int(time.time())

    if uttid is None:
      self.buf.extend(word_list)
      self.logger.debug("BUF: " + str(list(self.buf)))
      self.process_buffer()
      return

    if uttid != self.uttid:
      self.uttid = uttid
      if len(self.partial) > self.cutoff:
        self.buf.extend(self.partial[self.cutoff:])
        self.logger.debug("BUF: " + str(list(self.buf)))
      self.cutoff = 0
 
    self.partial = word_list
    self.logger.debug("PAR: " + str(list(self.partial[self.cutoff:])))
    self.process_buffer()


  def extract_command(self, buf):
    ntrigs = buf.count(self.trigger)

    # Don't bother extracting if no triggers or buffer is only the trigger
    if not ntrigs or (len(buf) == 1 and buf[0] == self.trigger):
      return (None, 0)
  
    # INVARIANT: At least one trigger is in buf to consume

    # If we're starting on a trigger, consume it 
    # and everything up to the next trigger, leaving   
    # the next one in the buffer
    start_trig = int(buf[0] == self.trigger)
    
    # Cut off the rest of the buffer if a trigger is present later
    if ntrigs > start_trig:
      trig_i = buf.index(self.trigger, start_trig)
      buf = buf[:trig_i]
     
    cmd_slice = [w for w in buf if w != self.trigger]
    if len(cmd_slice) and self.isValid(cmd_slice):
      return (cmd_slice, len(buf))
    else:
      return (None, len(buf))
    # POSTCONDITION: Exactly one trigger in the buffer has been consumed

  def process_buffer(self):
    while True:
      # Append partial transcriptions
      buf = list(self.buf)
      part = self.partial[self.cutoff:]
      #print buf, part

      # Try to pull out commands
      (cmd, words_used) = self.extract_command(buf+part)

      if words_used == 0: # We can't pull out any more commands
        break

      if cmd:
        self.callback(cmd)

      # Remove what was used from the actual queue and partials list
      buflen = len(buf)
      if words_used > buflen:
        self.cutoff += words_used - buflen
      for i in xrange(min(buflen, words_used)):
        self.buf.popleft()
      
  def inject(self, text, uttid = None):
    self.inj_queue.put(([word.strip(string.punctuation).lower() for word in text.split()], uttid))

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
    parser.evt.wait()
    parser.evt.clear()

  def uttid_test(parser, *args, **kwargs):
    time.sleep(0.1)
    print "UTTID TEST ", str(args), "expecting ", kwargs['results']
    parser.callback = gen_cb(kwargs['results'], cp.evt)
    for (uttid, text) in args:
      parser.inject(text, uttid)
    parser.evt.wait()
    parser.evt.clear()

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
  uttid_test(cp, (8, "jarvis"), (9, "jarvis"), (10, "projector"), results=[['projector']])
  uttid_test(cp, (11, "projector"), (12, "jarvis"), results=[['projector']])

  # Test command timeout
  def timeout_cb(s):
   raise Exception("Got command %s" % (s))
  cp.callback = timeout_cb
  cp.inject("jarvis", 999)
  time.sleep(cp.SPEECH_TIMEOUT + 0.1)
  cp.inject("projector", 1000)
  time.sleep(1.0)

  print "All tests passed"

