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

PORT=9201

class AudioCMD():
  PLAY = "play"
  MUSIC = "music"
  FADE_OUT = "fadeout"
  STOP_ALL = "stopall"
  SEP = '|'

  @classmethod
  def pack(self, cmd, path):
    return "%s%s%s\n" % (cmd, self.SEP, path)

  @classmethod
  def unpack(self, cmd):
    return cmd.strip().split(self.SEP)     
    
class AudioEngine(Controller):
  FADE_MS = 2500

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

  def music(self, mus):
    raise Exception("Unimplemented")

  def fadeout(self, snd):
    self.logger.info("Fading out %s" % snd)
    self.sounds[snd].fadeout(self.FADE_MS)

  def stopall(self):
    self.logger.info("Stopping all sounds")
    pygame.mixer.stop()

  def is_playing(self, snd):
    return (self.sounds[snd].get_num_channels() > 0)

class AudioServer(AudioEngine):
  def __init__(self, host, port=PORT, asset_path="Assets/Sounds/"):
    AudioEngine.__init__(self, asset_path)
    self.s = socket.socket()         # Create a socket object
    self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.s.settimeout(5.0)
    self.s.bind((host, port))        # Bind to the port
    self.s.listen(5)                 # Now wait for client connection.

    self.cmd_map = {
      AudioCMD.PLAY: self.play,
      AudioCMD.MUSIC: self.music,
      AudioCMD.FADE_OUT: self.fadeout,
      AudioCMD.STOP_ALL: self.stopall,
    }

  def handle_forever(self):
    last_img = None
    self.logger.info("Audio server started.")
    while True:
      try:
        c, addr = self.s.accept()     # Establish connection with client.
      except socket.timeout:
        continue
    
      msg = c.recv(1024)
      (cmd,snd) = AudioCMD.unpack(msg)
      self.cmd_map[cmd](snd)

class AudioController():
  def __init__(self, host, port=PORT):
    self.host = host
    self.port = port
    self.last_img = None

  def send_cmd(self, cmd, snd):
    s = socket.socket()         # Create a socket object
    s.connect((self.host, self.port))
    s.send(AudioCMD.pack(cmd, snd))
    s.close()

  def play(self, snd):
    self.send_cmd(AudioCMD.PLAY, snd)

  def music(self, snd):
    self.send_cmd(AudioCMD.MUSIC, snd)

  def fade_out(self, snd):
    self.send_cmd(AudioCMD.FADE_OUT, snd)

  def stop_all(self):
    self.send_cmd(AudioCMD.STOP_ALL, None)

def test_engine():
  con = AudioEngine()
  toplay = sys.argv[-1]
  con.play(toplay)
  c = pygame.time.Clock()
  while con.is_playing(toplay):
    c.tick(30)

def test_server():
  host = socket.gethostname()
  srv = AudioServer(host)
  srv.handle_forever()
  pass

if __name__ == '__main__': 
  import logging
  logging.basicConfig()
  test_server()
  #test_engine()
