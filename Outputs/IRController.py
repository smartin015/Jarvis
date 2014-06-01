from Controller import Controller

class IRController(Controller):
  BEGIN = 32766
  END = 32765

  def __init__(self, ser):
    Controller.__init__(self)
    self.ser = ser
  
  def send(self, fil):
    with open(fil, "r") as f:
      self.lines = f.read().split(', ')

    self.ser.write(struct.pack('>h', IRController.BEGIN))
    for l in lines:
      self.ser.write(struct.pack('>h', int(float(l))))
      self.ser.write(struct.pack('>h', IRController.END))

    # TODO: Make optional
    print self.ser.readline()
    self.logger.debug("Sent %s command" % (fil))

  def repeat(self, fil, ntimes):
    self.logger.debug("Sending %s, %d times" % (fil, ntimes))
    assert ntimes > 0
    for i in xrange(ntimes):
      self.send(fil)
