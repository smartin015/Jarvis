#!/usr/bin/env python
import logging
import threading
logging.basicConfig()
logging.addLevelName( logging.WARNING, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName( logging.ERROR, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR))

from Holodeck.Settings import Pipe as P
from Holodeck.Server import HolodeckServer
import time

class Holodeck(HolodeckServer):
  def __init__(self):
    self.devices = {
    }
    HolodeckServer.__init__(self)

  def get_pipeline_handlers(self):
    return [
    ]

  def get_pipeline_defaults(self):
    return {
    }

if __name__ == "__main__":
  h = Holodeck() 
  h.serve_forever()

