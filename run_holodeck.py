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

  # TODO: Should probably have an init profile per-machine. Maybe a class per machine, as in Decks?
  deckname = sys.argv[1]
  outputs = {}
  if deckname == "Jarvis":
    from run_jarvis import init_outputs
    outputs = init_outputs()

  mod = __import__('Holodeck.Decks', globals(), locals(), [deckname], -1)
  h = getattr(mod, sys.argv[1]).Holodeck(outputs)
  h.mainloop()

