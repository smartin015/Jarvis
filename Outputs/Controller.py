

class ArduinoController():

  def __init__(self, ser):
    self.ser = ser

    # TODO: Call-response style ping?
    if ser.read(1) == "A":
      print "Serial connection established"
    else:
      raise Exception("Invalid serial connection")

class IRController(ArduinoController):
  BEGIN = 32766
  END = 32765

  def send(self, fil):
    with f as open(fil):
      self.lines = f.read().split(', ')

    ser.write(struct.pack('>h', IRController.BEGIN))
    for l in lines:
      ser.write(struct.pack('>h', int(float(l))))
      ser.write(struct.pack('>h', IRController.END))

    # TODO: Make optional
    print ser.readline()

  def repeat(self, fil, ntimes):
    assert ntimes > 0
    for i in xrange(ntimes):
      self.send(fil)
