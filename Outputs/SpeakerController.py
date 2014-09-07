import subprocess
import threading
import os
from config import PATHS
from Outputs.Controller import Controller

class SpeakerController(Controller):
        
    def _play_sound_process(self, fil):
      print subprocess.call(["/usr/bin/aplay", fil])

    def play_multisound(self, files):
      # TODO: Subprocess call?
      os.system("sox %s /tmp/jarvisout.wav && aplay /tmp/jarvisout.wav" % (" ".join(files)))

    def play_sound(self, fil):
      # TODO: should probably safeguard this to prevent hijacking
      # TODO: Specify standard directory
      t1 = threading.Thread(target=self._play_sound_process, args=(PATHS['sound'] + fil,))
      t1.daemon = True
      t1.start()

