#!/usr/bin/env python
import logging
import threading
logging.basicConfig()
logging.addLevelName( logging.WARNING, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName( logging.ERROR, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR))

from Holodeck.pipe import Pipe as P
from Outputs.ScreenController import ScreenController
from Outputs.AudioController import AudioController
from Holodeck.holodeck_server import HolodeckServer
import time

class ToddHolodeck(HolodeckServer):
  def __init__(self):
    HolodeckServer.__init__(self)
    
    self.devices = {
      "proj_window": ScreenController(socket.gethostname()),
      "audio": AudioController(socket.gethostname()),
    }
    self.last_sounds = []

  def get_pipeline_handlers(self):
    return [
      ([P.WINDOWTOP, P.WINDOWBOT], self.window_leds),
      ([P.FLOOR], self.floor_leds),
      ([P.TOWER, P.RING], self.tower_ring),
      ([P.WINDOWIMG], self.window_img),
      ([P.WALLIMG], self.wall_img),
      ([P.LIGHTS], self.lights),
      ([P.SOUND], self.sound),
    ]

  def get_pipeline_defaults(self):
    return {
      P.WINDOWTOP:  [0,0,0],
      P.WINDOWBOT:  [0,0,0],
      P.FLOOR:      [0,0,0],
      P.TOWER:      [[0,0,0]]*NTOWER,
      P.RING:       [[0,0,0]]*NRING,
      P.WINDOWIMG:  None,
      P.WALLIMG:    None,
      P.LIGHTS:     False,
      P.SOUND:      [], 
      P.TEMP:       None,
    }

  def window_img(self, img):
    self.devices['proj_window'].zoom_to(img)
  
  def sound(self, sounds=[]):
    for s in sounds:
      if s not in self.last_sounds:
        self.devices['audio'].play(s)
    for s in self.last_sounds:
      if s not in sounds:
        self.devices['audio'].fade_out(s)
    self.last_sounds = sounds

if __name__ == "__main__":
  h = ToddHolodeck() 
  h.serve_forever()

