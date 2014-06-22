#!/usr/bin/env python
import logging
import threading
logging.basicConfig()
logging.addLevelName( logging.WARNING, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName( logging.ERROR, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR))

from Holodeck.Settings import Pipe as P
from serial import Serial
from Tests.TestSerial import TestSerial
from Outputs.RelayController import RelayController
from Outputs.RGBSingleController import RGBSingleController
from Outputs.RGBMultiController import RGBMultiController, RGBState, NTOWER, NRING
from Outputs.IRController import IRController
from Outputs.ScreenController import ScreenController
from Holodeck.Server import HolodeckServer
import time

class Holodeck(HolodeckServer):
  def __init__(self):
    self.devices = {
      "window": RGBSingleController(Serial("/dev/ttyUSB1", 9600)),
      "couch": RGBSingleController(Serial("/dev/ttyUSB0", 9600)),
      "tower": RGBMultiController(Serial("/dev/ttyACM0", 115200)),
      "proj": ScreenController(),
      "lights": RelayController(Serial("/dev/ttyUSB2", 9600)),
    }

    time.sleep(2.5) # Need delay at least this long for arduino to startup
    self.devices['tower'].setState(RGBState.STATE_MANUAL)
    time.sleep(1.0)

    self.img_path = "Assets/Images/"
    self.last_img = None

    HolodeckServer.__init__(self)

  def get_pipeline_handlers(self):
    return [
      #([P.WINDOWTOP, P.WINDOWBOT], self.window_leds),
      #([P.FLOOR], self.floor_leds),
      #([P.TOWER, P.RING], self.tower_ring),
      ([P.WALLIMG], self.wall_scrn),
      #([P.LIGHTS], self.lights),
    ]

  def get_pipeline_defaults(self):
    return {
      P.WINDOWTOP:  [0,0,0],
      P.WINDOWBOT:  [0,0,0],
      P.FLOOR:      [0,0,0],
      P.TOWER:      [[0,0,0]]*NTOWER,
      P.RING:       [[0,0,0]]*NRING,
      P.WALLIMG:    ScreenController.get_black_image(),
      P.LIGHTS:     False,
    }

  def window_leds(self, top, bot):
    self.devices['window'].write(top, bot)  

  def floor_leds(self, rgb):
    self.devices['couch'].write(rgb)
  
  def tower_ring(self, trgb, rrgb):
    for (i,c) in enumerate(trgb+rrgb):
      self.devices['tower'].manual_write(i, c)
    self.devices['tower'].manual_update()

  def lights(self, is_on):
    self.devices['lights'].set_state(is_on)

  def wall_scrn(self, scrn):
    self.devices['proj'].set_scrn(scrn)

if __name__ == "__main__":
  h = Holodeck() 
  h.serve_forever()

