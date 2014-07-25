import json
import threading
import socket
import logging
import threading
import subprocess
from config import REMOTES
from Monitor.monitor import ProcessMonitor
import win32api
import win32con

def get_port_for(host):
  port = None
  for r in REMOTES:
    if r.host == host:
      return r.port
  
  raise Exception("Remote \"%s\" not found in config" % host)

def send_remote_cmd(host, name, cmd):    
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.sendto(name + RemoteClient.SEP + cmd, (host, get_port_for(host)))

class RemoteClient(threading.Thread):
  SEP = '|'

  def __init__(self):
    super(RemoteClient,self).__init__()
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.setLevel(logging.DEBUG)
    
    self.s = None
    self.host = socket.gethostname()
    self.port = get_port_for(self.host)
    
    self.procs = {}
      
  def __del__(self):
    if self.s:
      self.s.close()

  def execute(self, cmd):
    (name, cmd) = cmd.split(self.SEP)
    self.logger.warn("[%s] Running \"%s\"" % (name, cmd))
    if self.procs.get(name):
      if cmd != "QUIT":
        print "Process already running!"
      else:
        #self.procs[name].shutdown() # Only works in linux
        try:
          print "TODO: Graceful shutdown"
          # This doesn't work.
          win32api.GenerateConsoleCtrlEvent(win32con.CTRL_C_EVENT, 0)
          self.procs[name].proc.wait()
        except KeyboardInterrupt:
          print "ignoring ctrl c"
        self.procs[name].join()
        del self.procs[name]
    else:
      if cmd == "QUIT":
        print "Process wasn't started!"
      else:
        self.procs[name] = ProcessMonitor(cmd, auto_restart=False)
        self.procs[name].start()
      
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
      
      self.execute(msg)
      
        
if __name__ == "__main__":
  logging.basicConfig()
  cli = RemoteClient()
  cli.daemon = True
  cli.start()
  
  raw_input("Enter to exit")
