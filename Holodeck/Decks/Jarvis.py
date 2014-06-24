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
from Outputs.ScreenController import ScreenController as scl
from Holodeck.Server import HolodeckServer
import time

class Holodeck(HolodeckServer):
  def __init__(self):
    self.devices = {
      "window": RGBSingleController(Serial("/dev/ttyUSB1", 9600)),
      "couch": RGBSingleController(Serial("/dev/ttyUSB0", 9600)),
      "tower": RGBMultiController(Serial("/dev/ttyUSB3", 115200)),
      "proj": scl(),
      "lights": RelayController(Serial("/dev/ttyUSB2", 9600)),
    }

    # TODO: Base this on arduino communication to the computer
    time.sleep(2.5) # Need delay at least this long for arduino to startup
    self.devices['tower'].setState(RGBState.STATE_MANUAL)
    time.sleep(1.0)

    self.img_path = "Holodeck/Images/"
    self.last_img = None

    HolodeckServer.__init__(self)

  def mainloop(self):
    t = threading.Thread(target = self.serve_forever)
    t.daemon = True
    t.start()

    self.devices['proj'].mainloop()

  def get_pipeline_handlers(self):
    return [
      ([P.WINDOWTOP, P.WINDOWBOT], self.window_leds),
      ([P.FLOOR], self.floor_leds),
      ([P.TOWER, P.RING], self.tower_ring),
      ([P.WALLIMG], self.wall_scrn),
      ([P.LIGHTS], self.lights),
    ]

  def get_pipeline_defaults(self):
    return {
      P.WINDOWTOP:  [0,0,0],
      P.WINDOWBOT:  [0,0,0],
      P.FLOOR:      [0,0,0],
      P.TOWER:      [[0,0,0]]*NTOWER,
      P.RING:       [[0,0,0]]*NRING,
      P.WALLIMG:    ["right","mountain","clear","day"],
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
    self.devices['proj'].set_scrn(scl.loadimg(self.img_path + scrn[0] + "/" + scrn[1] + "_" + scrn[2] + "_" + scrn[3] + ".jpg"))

    '''
    self.devices['proj'].set_scrn(scrn)
    '''
    

  def trans_wall_img(self, screen):
    final = self.steady_mapping[P.WALLIMG](screen)
    if not self.screen_transition:
      self.transition_screen = screen.copy()
      self.screen_transition = scl.gen_sweep(screen, final, self.transition_screen)
    return self.handle_screen_transition(final)
    
  def trans_window_img(self, screen):
    final = self.steady_mapping[P.WINDOWIMG](screen)
    if not self.screen_transition:
      self.transition_screen = screen.copy()
      self.screen_transition = scl.gen_zoom(screen, final, self.transition_screen)
    return self.handle_screen_transition(final)


if __name__ == "__main__":
  h = Holodeck() 
  h.mainloop()

