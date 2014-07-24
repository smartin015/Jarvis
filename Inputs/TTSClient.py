import json
import threading
import socket
import logging
from TTSServer import TTSServer
import time

class TTSClient(threading.Thread):
  RETRY_INTERVAL = 5.0
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

  def connect(self):
    self.logger.info("Attempting to connect...")
    while True:
      try:
        self.s = socket.create_connection((self.host,self.port)).makefile()
        self.logger.debug("Connected")
        return
      except:
        self.logger.error("Connection failed. Retrying in %d seconds..." % self.RETRY_INTERVAL)
        time.sleep(self.RETRY_INTERVAL)
        
  def run(self):
    self.connect()

    while True: 
      try:
        msg = self.s.readline()
        if not msg:
          self.logger.warn("Server connection closed.")
          self.connect()
          continue
        
        (uttid, text) = msg.split(TTSServer.SEP)
        self.logger.debug("%s: %s" % (uttid, (text[:40] + '..') if len(text) > 40 else text.strip()))
        self.callback(text, uttid)
      except:
        self.logger.warn("Connection closed")
        return
