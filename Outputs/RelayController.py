from Controller import Controller

class RelayController(Controller):
  
  def __init__(self, ser):
    Controller.__init__(self)
    self.ser = ser
    self.is_on = False
    self.off()

  def is_on(self):
    return self.is_on

  def on(self):
    self.ser.write('T')
    self.is_on = True

  def off(self):
    self.ser.write('F')
    self.is_on = False

  def toggle(self):
    if self.is_on:
      self.off()
    else:
      self.on()
