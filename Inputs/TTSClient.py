import json
import threading
import socket
import logging

class TTSClient(threading.Thread):
  def __init__(self, name, host, port, callback):
    threading.Thread.__init__(self)
    self.logger = logging.getLogger(name)
    self.logger.setLevel(logging.DEBUG)
    self.host = host
    self.port = port
    self.callback = callback
    self.s = None

  def __del__(self):
    if self.s:
      self.s.close()

  def run(self):
    try:
      self.s = socket.create_connection((self.host,self.port)).makefile()
      self.logger.debug("Connected")
    except:
      self.logger.error("Connection failed")
      return

    while True: #TODO: could be done better
      try:
        msg = self.s.readline()
        if not msg:
          self.logger.warn("Server connection closed")
          return

        self.logger.debug("%s" % ((msg[:40] + '..') if len(msg) > 40 else msg.strip()))
        self.callback(msg)
      except:
        self.logger.warn("Connection closed")
        return
