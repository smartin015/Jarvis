#!/usr/bin/env python
# Credit to Christopher Arndt:
# http://code.activestate.com/recipes/521884-play-sound-files-with-pygame-in-a-cross-platform-m/

import sys
import pygame
import os
import socket
from Controller import Controller

# global constants
FREQ = 44100   # same as audio CD
BITSIZE = -16  # unsigned 16 bit
CHANNELS = 2   # 1 == mono, 2 == stereo
BUFFER = 1024  # audio buffer size in no. of samples
    
class AudioController(Controller):
  FADE_MS = 5000
  FADE_FAST_MS = 2500

  def __init__(self, asset_path="Assets/Sounds/"):
    Controller.__init__(self)
    pygame.mixer.init(FREQ, BITSIZE, CHANNELS, BUFFER)

    self.logger.info("Loading assets...")
    self.sounds = {}
    for dirpath, dirnames, filenames in os.walk(asset_path):
      for sndfil in filenames:
          print sndfil
          self.sounds[sndfil.split('.')[0]] = pygame.mixer.Sound(os.path.join(dirpath,sndfil))
    
      
    self.logger.info("All assets loaded.")

  def get_asset_list(self):
    return self.sounds.keys()

  def play(self, snd):
    self.logger.info("Playing %s" % snd)
    self.sounds[snd].play() 

  def fadein(self, snd, loops=-1):
    self.logger.info("Playing ambient %s" % snd)
    self.sounds[snd].play(loops=loops, fade_ms=self.FADE_MS) 
    
  def music(self, mus):
    raise Exception("Unimplemented")

  def fadeout_fast(self, snd):
    self.logger.info("Fading out %s" % snd)
    self.sounds[snd].fadeout(self.FADE_FAST_MS)
    
  def fadeout(self, snd):
    self.logger.info("Fading out %s" % snd)
    self.sounds[snd].fadeout(self.FADE_MS)

  def stopall(self):
    self.logger.info("Stopping all sounds")
    pygame.mixer.stop()

  def is_playing(self, snd):
    return (self.sounds[snd].get_num_channels() > 0)

  
if __name__ == '__main__': 
  import logging
  logging.basicConfig()
  con = AudioController()
  toplay = sys.argv[-1]
  con.play(toplay)
  c = pygame.time.Clock()
  while con.is_playing(toplay):
    c.tick(30)

