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

ON_POSIX = 'posix' in sys.builtin_module_names
def enqueue_output(out, queue):
  for line in iter(out.readline, b''):
    queue.put((out,line))
  queue.put((None,out))
  out.close()

class ProcessMonitor(threading.Thread):
  TIMEOUT = 10.0

  def __init__(self, script, host = None, port=PORT, auto_restart = True):
    threading.Thread.__init__(self)
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.setLevel(logging.DEBUG)
    self.script = script
    self.auto_restart = auto_restart
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.host = host if host else socket.gethostname()
    self.port = port
    self.last_time = time.time()
    self.q = Queue.Queue()
    
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

      try:
        (fd, line) = self.q.get(timeout=self.TIMEOUT)
        if not fd:
          self.logger.warn("FD %d exited" % fd)
        
        if fd == self.proc.stderr:
          sys.stderr.write(line+"\n")
        else:
          sys.stdout.write(line+"\n")
        
        self.last_time = time.time()

        if "DEBUG" not in line and "INFO" not in line:
          self.broadcast(json.dumps({"type": "delta", "name": self.script, "msg": line}))
      except Queue.Empty: 
        pass
        
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
    self.proc = subprocess.Popen(["python"] + self.script.split(), stdout=PIPE, stderr=PIPE, stdin=PIPE, bufsize=1, close_fds=ON_POSIX)
    proc_stdout = threading.Thread(target=enqueue_output, args=(self.proc.stdout, self.q))
    proc_stdout.daemon = True
    proc_stderr = threading.Thread(target=enqueue_output, args=(self.proc.stderr, self.q))
    proc_stderr.daemon = True
    proc_stdout.start()
    proc_stderr.start()

  def stop(self, block = False):
    self.logger.info("Stopping")
    self.proc.send_signal(signal.SIGINT)   
    if block:
      self.proc.wait()
    
  def shutdown(self):
    self.auto_restart = False
    self.stop(block=True)

  def inject(self, txt):
    self.proc.stdin.write(txt)

if __name__ == "__main__":
  logging.basicConfig()
  
  if len(sys.argv) != 2:
    print "Usage: %s <process.py>" % sys.argv[0]
    sys.exit(-1)

  pmon = ProcessMonitor(sys.argv[1])
  try:
    pmon.start()
    while True:
      pmon.inject(raw_input())
  finally:
    print "Server shut down, waiting for child processes..."
    pmon.shutdown()
    pmon.join()
    print "All processes exited"
