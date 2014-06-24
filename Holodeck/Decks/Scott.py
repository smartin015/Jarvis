#!/usr/bin/env python
import logging
import threading
logging.basicConfig()
logging.addLevelName( logging.WARNING, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName( logging.ERROR, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR))

from Holodeck.Settings import Pipe as P
from Outputs.ScreenController import ScreenController as scl
from Outputs.AudioController import AudioController
from Holodeck.Server import HolodeckServer
import time

class Holodeck(HolodeckServer):
  def __init__(self):
    self.devices = {
      "proj": scl(),
      "audio": AudioController(asset_path="Holodeck/Sounds/"),
    }
    self.last_sounds = ([],[])

    HolodeckServer.__init__(self)

  def mainloop(self):
    t = threading.Thread(target=self.serve_forever)
    t.daemon = True
    t.start()
    
    self.devices['proj'].mainloop()
    
  def get_pipeline_handlers(self):
    return [
      ([P.WINDOWIMG], self.window_scrn),
      ([P.SOUND], self.sound),
    ]

  def new_sound_val(self):
    return ([],[])
    
  def get_pipeline_defaults(self):
    return {
      P.WINDOWIMG:  ["front","mountain","clear","day"],
      P.SOUND:      self.new_sound_val, 
    }

  def window_scrn(self, scrn):
    self.devices['proj'].set_scrn(scl.loadimg(self.img_path + scrn[0] + "/" + scrn[1] + "_" + scrn[2] + "_" + scrn[3] + ".jpg"))
     
  def sound(self, sounds):
    (ambient, effects) = sounds
    (last_ambient, last_effects) = self.last_sounds
    for s in effects:
      if s not in last_effects:
        print "playing", s
        self.devices['audio'].play(s)
        
    for s in ambient:
      if s not in last_ambient:
        print "fading in", s
        self.devices['audio'].fadein(s)
        
    for s in last_ambient:
      if s not in ambient:
        print "fading out", s
        self.devices['audio'].fadeout(s)
        
    for s in last_effects:
      if s not in effects:
        print "stopping", s
        self.devices['audio'].fadeout_fast(s)
    self.last_sounds = sounds
    
  

if __name__ == "__main__":
  h = Holodeck()  
  h.mainloop()

