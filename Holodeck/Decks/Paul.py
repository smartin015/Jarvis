#!/usr/bin/env python
from Jarvis import Holodeck as JarvisHolodeck
import time

class Holodeck(JarvisHolodeck):
  
  def serve_forever(self):
    self.deck.handle({'beach': True})
    time.sleep(2.0)
    self.deck.handle({'day': True})
    raw_input("Enter to exit:")


if __name__ == "__main__":
  deck = Holodeck()
  deck.serve_forever()

