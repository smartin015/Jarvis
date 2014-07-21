import logging
import subprocess
import os
import select
import threading
import signal
import Queue
import sys
import socket
import json
import time
from monitor_server import UDP_PORT as PORT

class LineReader(object):
  def __init__(self, fd, is_err=False):
    self._fd = fd
    self._buf = ''
    self.is_err = is_err

  def is_error(self):
    return self.is_err

  def fileno(self):
    return self._fd

  def readlines(self):
    data = os.read(self._fd, 4096)
    if not data:
        # EOF
        return None
    self._buf += data
    if '\n' not in data:
        return []
    tmp = self._buf.split('\n')
    lines, self._buf = tmp[:-1], tmp[-1]
    return lines

class ProcessMonitor():
  def __init__(self, script, host = None, port=PORT, auto_restart = True):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.setLevel(logging.DEBUG)
    self.script = script
    self.auto_restart = auto_restart
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.host = host if host else socket.gethostname()
    self.port = port
    self.last_time = time.time()

  def run(self):
    self.start_script()
    while True:
      self.proc.poll()
      if self.proc.returncode is not None:
        self.logger.warn("Process exited (code %d)" % self.proc.returncode)
        self.broadcast(json.dumps({
          "type": "delta", 
          "name": self.script, 
          "msg": "Process exited (code %d)" % self.proc.returncode
        }))
        if self.auto_restart:
          self.start_script()
        else:
          self.logger.warn("Process monitor exiting")
          return

      ready, _, _ = select.select(self.readable, [], [], 10.0)
      if ready:
        for stream in ready:
          lines = stream.readlines()
          if lines is None:
            # got EOF on this stream
            self.logger.warn("Stream %d closed" % stream.fileno())
            self.readable.remove(stream)
            continue
          for line in lines:
            if stream.is_error():
              sys.stderr.write(line+"\n")
            else:
              sys.stdout.write(line+"\n")
            
            self.last_time = time.time()

            if "WARNING" in line or "ERROR" in line:
              self.broadcast(json.dumps({"type": "delta", "name": self.script, "msg": line}))

      self.broadcast(json.dumps({
        "type": "heartbeat", 
        "name": self.script, 
        "time": self.last_time
      }))

  def broadcast(self, txt):
    self.socket.sendto(txt, (self.host, self.port))

  def start_script(self):
    self.logger.info("Starting")
    PIPE = subprocess.PIPE
    self.proc = subprocess.Popen(["/usr/bin/python", self.script], bufsize=0, stdout=PIPE, stderr=PIPE)
    proc_stdout = LineReader(self.proc.stdout.fileno())
    proc_stderr = LineReader(self.proc.stderr.fileno(), is_err=True)
    self.readable = [proc_stdout, proc_stderr] 

  def stop(self, block = False):
    self.logger.info("Stopping")
    self.proc.send_signal(signal.SIGINT)   
    if block:
      self.proc.wait()
    
  def shutdown(self):
    self.auto_restart = False
    self.stop(block=True)

if __name__ == "__main__":
  logging.basicConfig()
  
  if len(sys.argv) != 2:
    print "Usage: %s <proccess.py>" % sys.argv[0]
    sys.exit(-1)

  pmon = ProcessMonitor(sys.argv[1])
  try:
    pmon.run()
  finally:
    print "Server shut down, waiting for child processes..."
    pmon.shutdown()
    print "All processes exited"
