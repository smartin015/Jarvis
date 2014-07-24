#!/usr/bin/env python
from Outputs.RGBMultiController import RGBState, NTOWER, NRING
from Holodeck.Decks.DeckBase import HolodeckBase
from Holodeck.Settings import Pipe as P
import time

class Holodeck(HolodeckBase):
  EMPTY_IMG = ["", "clear", "day"]
  IMG_PATH = "Holodeck/Images/right/"

  def __init__(self, devices):
    devices['tower'].setState(RGBState.STATE_MANUAL)
    time.sleep(1.0)
    HolodeckBase.__init__(self, devices)

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
      P.WALLIMG:    list(self.EMPTY_IMG),
      P.LIGHTS:     False,
    }

if __name__ == "__main__":
  from run_jarvis import init_outputs
  devices = init_outputs()
  # TODO: Base this on arduino communication to the computer
  h = Holodeck(devices) 
  h.setup()
  h.mainloop()

