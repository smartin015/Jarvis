from RelayController import RelayController
import threading

class ACController(RelayController):

  def __init__(self, ser, hysteresis = 2):
    RelayController.__init__(self, ser)
    self.hyst = hysteresis
    # TODO: Start thread that monitors temperature

  def set_temp(self, temp):
    raise Exception("Unimplemented")

  def read_temp(self):
    raise Exception("Unimplemented")

  def monitor_temp(self):
    while True:
      temp = self.read_temp()
      time.sleep(10.0)
