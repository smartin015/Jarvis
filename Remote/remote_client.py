import json
import threading
import socket
import logging
import threading
import os
from config import REMOTES

def get_port_for(host):
  port = None
  for r in REMOTES:
    if r.host == host:
      return r.port
  
  raise Exception("Remote \"%s\" not found in config" % host)

def send_remote_cmd(host, cmd):    
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.sendto(cmd, (host, get_port_for(host)))

class RemoteClient(threading.Thread):
  def __init__(self):
    super(RemoteClient,self).__init__()
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.setLevel(logging.DEBUG)
    
    self.s = None
    self.host = socket.gethostname()
    self.port = get_port_for(self.host)
      
  def __del__(self):
    if self.s:
      self.s.close()

  def execute(self, cmd):
    print os.popen("python Scripts/%s" % cmd).read()
      
  def run(self):
    try:
      self.s = sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      sock.bind((self.host, self.port))
      self.logger.debug("Listening")
    except:
      self.logger.error("Connection failed")
      return

    while True: #TODO: could be done better
      try:
        msg, addr = sock.recvfrom(1024)
        if not msg:
          self.logger.warn("Server connection closed")
          return
      except:
        self.logger.warn("Connection closed")
        return
      
      self.logger.warn("Running \"%s\"" % msg)
      self.execute(msg)
      
        
if __name__ == "__main__":
  logging.basicConfig()
  cli = RemoteClient()
  cli.daemon = True
  cli.start()
  
  raw_input("Enter to exit")