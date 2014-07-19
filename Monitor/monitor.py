import logging
import subprocess
import os
import select
import threading
import signal
import Queue

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

class ProcessMonitor(threading.Thread):
  def __init__(self, script, callback, auto_restart = True, ):
    threading.Thread.__init__(self)
    self.logger = logging.getLogger("procmon(%s)" % (script))
    self.logger.setLevel(logging.DEBUG)
    self.script = script
    self.callback = callback
    self.auto_restart = auto_restart

  def run(self):
    self.start_script()
    while True:
      self.proc.poll()
      if self.proc.returncode is not None:
        self.logger.warn("Process exited (code %d)" % self.proc.returncode)
        if self.auto_restart:
          self.start_script()
        else:
          self.logger.warn("Process monitor exiting")
          return

      ready, _, _ = select.select(self.readable, [], [], 10.0)
      if not ready:
        continue
      for stream in ready:
        lines = stream.readlines()
        if lines is None:
          # got EOF on this stream
          self.readable.remove(stream)
          continue
        for line in lines:
          self.callback(self.script, stream.is_error(), line)

  def start_script(self):
    self.logger.info("Starting")
    PIPE = subprocess.PIPE
    self.proc = subprocess.Popen(["/usr/bin/python", self.script], bufsize=0, stdout=PIPE, stderr=PIPE)
    proc_stdout = LineReader(self.proc.stdout.fileno())
    proc_stderr = LineReader(self.proc.stderr.fileno(), is_err=True)
    self.readable = [proc_stdout, proc_stderr] 

  def stop(self):
    self.logger.info("Stopping")
    self.proc.send_signal(signal.SIGINT)   
    
  def shutdown(self):
    self.auto_restart = False
    self.stop()

if __name__ == "__main__":
  logging.basicConfig()

  def print_cb(name, is_error, line):
    print "%s %s %s" % (name, is_error, line)
      
  #TODO: Put in DB
  MONITORS = (
    #ProcessMonitor("run_tts.py", print_cb),
    #ProcessMonitor("main.py", print_cb),
    ProcessMonitor("run_sockets.py", print_cb),
  )

  # Start each process 
  for mon in MONITORS:
    mon.start()

  raw_input("Enter to exit")

  for mon in MONITORS:
    mon.stop()

