#!/usr/bin/env python
from Jarvis import Holodeck as JarvisHolodeck

class Holodeck(JarvisHolodeck):
  
  def serve_forever(self):
    self.deck.handle({'beach': True})
    raw_input("Enter to exit:")


if __name__ == "__main__":
  deck = Holodeck()
  deck.serve_forever()

