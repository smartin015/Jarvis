from Controller import Controller

class RelayController(Controller):
  
  def __init__(self, ser):
    Controller.__init__(self)
    self.ser = ser
    self.is_on = False
    self.off()

  def is_on(self):
    return self.is_on

  def set_state(self, isOn):
    if isOn:
      self.on()
    else:
      self.off()

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


if __name__ == "__main__":
  import serial
  import time
  from Inputs.USBDiscovery import get_connected_usb_devices
  usb_devices = get_connected_usb_devices()

  ser = serial.Serial(usb_devices["A602QORA"], 9600)
  time.sleep(1.5)
  
  con = RelayController(ser)

  print "Lights on"
  con.on()
  time.sleep(1.0)
  print "Lights off"
  con.off()
