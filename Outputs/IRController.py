from ArduinoController import ArduinoController

class IRController(ArduinoController):
  BEGIN = 32766
  END = 32765

  def send(self, fil):
    with f as open(fil):
      self.lines = f.read().split(', ')

    self.ser.write(struct.pack('>h', IRController.BEGIN))
    for l in lines:
      self.ser.write(struct.pack('>h', int(float(l))))
      self.ser.write(struct.pack('>h', IRController.END))

    # TODO: Make optional
    print self.ser.readline()

  def repeat(self, fil, ntimes):
    assert ntimes > 0
    for i in xrange(ntimes):
      self.send(fil)
