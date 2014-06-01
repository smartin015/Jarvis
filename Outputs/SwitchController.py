from Controller import Controller

class SwitchController(Controller):
  
  def __init__(self, ser):
    Controller.__init__(self)
    self.ser = ser
    self.off()

  def is_on(self):
    return self.is_on

  def on(self):
    self.ser.write(chr(1))
    self.is_on = True

  def off(self):
    self.ser.write(chr(0))
    self.is_on = False

  def toggle(self):
    if self.is_on:
      self.off()
    else:
      self.on()
