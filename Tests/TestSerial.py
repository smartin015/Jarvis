import logging

class TestSerial():
  def __init__(self, port, baud):
    logging.debug("Test Serial: %s @ %s" % (port, baud))
    self.port = port

  def write(self, data):
    logging.debug("%s: %s" % (self.port, data))
  
  def read(self, nbytes = -1):
    logging.debug("%s: reading character")
    return "A"
    
  def close(self):
    pass

  def open(self):
    pass

  def readline(self):
    return self.read()
    
