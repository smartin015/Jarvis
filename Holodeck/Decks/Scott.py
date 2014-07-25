#!/usr/bin/env python
from Holodeck.Decks.DeckBase import HolodeckBase
from Outputs.AudioController import AudioController
from Holodeck.Settings import Pipe as P
import time

class Holodeck(HolodeckBase):
  EMPTY_IMG = ["", "clear", "day"]
  IMG_PATH = "Holodeck/Images/front/"

  def __init__(self, devices):
    devices['audio'] = AudioController(asset_path="Holodeck/Sounds/")
    HolodeckBase.__init__(self)

  def get_pipeline_handlers(self):
    return [
      ([P.WINDOWIMG], self.window_scrn),
      ([P.SOUND], self.sound),
    ]

  def get_pipeline_defaults(self):
    return {
      P.WINDOWIMG:  list(self.EMPTY_IMG),
      P.SOUND:      ([], []),
    }

if __name__ == "__main__":
  h = Holodeck()  
  h.mainloop()

