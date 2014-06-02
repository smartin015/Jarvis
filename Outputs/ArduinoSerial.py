import serial 

class ArduinoSerial(serial.Serial):

  def __init__(self, port, baud):
    serial.Serial.__init__(self, port, baud)
    self.init()
 
  def init(self):
    self.close()
    self.open()

    # TODO: Call-response style ping?
    if self.read(1) == "A":
      print "Serial connection established"
    else:
      raise Exception("Invalid serial connection")



        
