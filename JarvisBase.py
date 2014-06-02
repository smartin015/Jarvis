import logging
from os import system


class JarvisBase():
  def __init__(self):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.setLevel(logging.DEBUG)

  def play_sound(self, fil):
    # TODO: should probably safeguard this to prevent hijacking
    system("aplay %s" % fil)
