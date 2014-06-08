import serial 

class ArduinoSerial(serial.Serial):
 
  def open(self):
    self.close()
    serial.Serial.open(self)

    # TODO: Call-response style ping?
    c = self.read(1)
    if c != "A":
      self.close()
      raise Exception("Invalid serial connection - starting bit was %s" % c)



        
