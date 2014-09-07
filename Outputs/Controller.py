from JarvisBase import JarvisBase
from RobustChannel import RobustJSONServer, RobustJSONClient
import time
import threading
import Queue

class Controller(JarvisBase):
  MAX_CMD_QUEUE_LEN = 5

  def __init__(self):
    JarvisBase.__init__(self)
    self._cmd_queue = Queue.Queue(maxsize=self.MAX_CMD_QUEUE_LEN)
    self._cmd_thread = threading.Thread(target=self._eval_daemon)
    self._cmd_thread.daemon = True
    self._cmd_thread.start()

  def _eval_daemon(self):
    time.sleep(2.0) # Give us time to initialize
    while True:
      (fun, args, kwargs) = self._cmd_queue.get(block=True)
      try:
        fun(*args, **kwargs)
      except:
        traceback.print_exc()

  def _push_cmd(self, fun_str, args, kwargs):
    try:
      fun = getattr(self, fun_str)
      self._cmd_queue.put((fun, args, kwargs))
    except AttributeError:
      self.logger.error("No function %s in %s" % (fun_str, self.__class__.__name__))
      return False


class ControllerServer(RobustJSONServer):
  DEFAULT_PORT = 2598
  """ The Controller server is in charge of buffering and driving output 
      to all controllable devices (lights, projector, etc.). 

      The controller also maintains state. Restarting the controller server
      will put the system in a safe state (i.e. all loads turned off).
  """

  def __init__(self, server_address, outputs):
    RobustJSONServer.__init__(self, server_address)
    self.outputs = outputs
    
  def handle(self, data):
    try:
      (output, fun_str, args, kwargs) = data
    except ValueError, TypeError:
      self.logger.error("Invalid data type for controller - data is: %s" % type(data))
      return (False, None)

    out = self.outputs.get(output)
    if not out:
      self.logger.error("Unknown Output \"%s\"" % (output,))
      return (False, None)
    out._push_cmd(fun_str, args, kwargs)
    self.logger.debug("Pushed command to \"%s\"" % (output,))


class ControllerClient(RobustJSONClient):
   def cmd(self, output, fun_str, args=[], kwargs={}):
     self.send((output, fun_str, args, kwargs))

if __name__ == "__main__":
  from socket import gethostname

  cli = ControllerClient((gethostname(), ControllerServer.DEFAULT_PORT))
  
  while True:
    timer.sleep(1.0)
    cli.cmd("mainlight", "toggle")

