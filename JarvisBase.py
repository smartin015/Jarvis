import logging
import subprocess
import threading

class JarvisBase():
  def __init__(self):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.setLevel(logging.DEBUG)

  def _play_sound_process(self, fil):
    print subprocess.call(["/usr/bin/aplay", fil])

  def play_sound(self, fil):
    # TODO: should probably safeguard this to prevent hijacking
    t1 = threading.Thread(target=self._play_sound_process, args=(fil,))
    t1.daemon = True
    t1.start()
