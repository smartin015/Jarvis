import logging
import subprocess
import os
import threading

class JarvisBase():
  def __init__(self):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.setLevel(logging.DEBUG)

