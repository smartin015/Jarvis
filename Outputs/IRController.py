from Controller import Controller
import struct

class IRController(Controller):
  BEGIN = 32766
  END = 32765

  def __init__(self, ser):
    Controller.__init__(self)
    self.ser = ser
  
  def send(self, fil):
    try:
      self.logger.debug("Initializing serial")
      self.ser.open()
      self.logger.debug("Serial ready, sending file")
      with open(fil, "r") as f:
        lines = f.read().split(', ')

      self.ser.write(struct.pack('>h', IRController.BEGIN))
      for l in lines:
        self.ser.write(struct.pack('>h', int(float(l))))
      
      self.ser.write(struct.pack('>h', IRController.END))

      response = self.ser.readline()
      self.logger.debug("Sent %s command, response %s" % (fil, response))
    finally:
      self.ser.close()
