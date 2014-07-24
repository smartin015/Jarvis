#!/usr/bin/env python
import logging
import sys

if __name__ == "__main__":

  logging.basicConfig()
  logging.addLevelName( logging.WARNING, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
  logging.addLevelName( logging.ERROR, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR))

  from run_jarvis import init_outputs
  if len(sys.argv) != 2:
    raise Exception("Usage: %s <holodeck>" % sys.argv[0])

  mod = __import__('Holodeck.Decks', globals(), locals(), [sys.argv[1]], -1)
  h = getattr(mod, sys.argv[1]).Holodeck(init_outputs())
  h.mainloop()

