class ArduinoController():

  def __init__(self, ser):
    self.ser = ser

    # TODO: Call-response style ping?
    if ser.read(1) == "A":
      print "Serial connection established"
    else:
      raise Exception("Invalid serial connection")
