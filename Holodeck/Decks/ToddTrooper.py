#!/usr/bin/env python
import logging
import threading
logging.basicConfig()
logging.addLevelName( logging.WARNING, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName( logging.ERROR, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR))

from Holodeck.Settings import Pipe as P
from Outputs.ScreenController import ScreenController
from Outputs.AudioController import AudioController
from Holodeck.Server import HolodeckServer
import time

class Holodeck(HolodeckServer):
  def __init__(self):
    self.devices = {
      "proj": ScreenController(),
      "audio": AudioController(),
    }
    self.last_sounds = []
    self.last_img = None
    self.img_path = "Assets/Images/"

    HolodeckServer.__init__(self)

  def mainloop(self):
    t = threading.Thread(target=self.serve_forever)
    t.daemon = True
    t.start()

    self.devices['proj'].mainloop()

  def get_pipeline_handlers(self):
    return [
      ([P.WINDOWIMG], self.window_img),
      ([P.SOUND], self.sound),
    ]

  def get_pipeline_defaults(self):
    return {
      P.WINDOWIMG:  None,
      P.SOUND:      [], 
    }

  def window_img(self, img):
    # TODO: Zoom
    if img != self.last_img:
      img_data = self.devices['proj'].loadimg(self.img_path + img)
      self.devices['proj'].setimg(img_data)
      self.last_img = img
  
  def sound(self, sounds=[]):
    for s in sounds:
      if s not in self.last_sounds:
        self.devices['audio'].play(s)
    for s in self.last_sounds:
      if s not in sounds:
        self.devices['audio'].fadeout(s)
    self.last_sounds = sounds

if __name__ == "__main__":
  h = Holodeck() 
  h.mainloop()

