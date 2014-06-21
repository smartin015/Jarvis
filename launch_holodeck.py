#!/usr/bin/env python
import logging
import sys

logging.basicConfig()
logging.addLevelName( logging.WARNING, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName( logging.ERROR, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR))

from Holodeck.Decks import *

def str_to_class(str):
  return reduce(getattr, str.split("."), sys.modules[__name__]) 

if __name__ == "__main__":
  if len(sys.argv) != 2:
    raise Exception("Usage: %s <holodeck>" % sys.argv[0])

  h = str_to_class(sys.argv[1]).Holodeck() 
  h.serve_forever()

