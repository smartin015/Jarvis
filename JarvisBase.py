import logging

class JarvisBase():
  def __init__(self):
    self.logger = logging.getLogger(type(self).__name__)