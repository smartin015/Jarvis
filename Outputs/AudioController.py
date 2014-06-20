#!/usr/bin/env python
# Credit to Christopher Arndt:
# http://code.activestate.com/recipes/521884-play-sound-files-with-pygame-in-a-cross-platform-m/

import sys
import pygame
import os
from Controller import Controller

# global constants
FREQ = 44100   # same as audio CD
BITSIZE = -16  # unsigned 16 bit
CHANNELS = 2   # 1 == mono, 2 == stereo
BUFFER = 1024  # audio buffer size in no. of samples

class AudioController(Controller):
  def __init__(self, asset_path="Assets/Sounds/"):
    Controller.__init__(self)
    pygame.mixer.init(FREQ, BITSIZE, CHANNELS, BUFFER)

    self.logger.info("Loading assets...")
    self.sounds = {}
    for sndfil in os.listdir(asset_path):
      print sndfil
      self.sounds[sndfil.split('.')[0]] = pygame.mixer.Sound(asset_path+sndfil)
    self.logger.info("All assets loaded.")

  def get_asset_list(self):
    return self.sounds.keys()

  def play(self, snd):
    """ Loads from disk, then plays """
    self.logger.info("Playing %s" % snd)
    self.sounds[snd].play()

  def playing(self):
    return pygame.mixer.get_busy()

if __name__ == '__main__': 
  import logging
  logging.basicConfig()
  con = AudioController()

  toplay = sys.argv[-1]
  con.play(toplay)
  c = pygame.time.Clock()
  while con.playing():
    c.tick(30)
