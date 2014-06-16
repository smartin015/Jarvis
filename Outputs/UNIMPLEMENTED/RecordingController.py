from Outputs.Controller import Controller

class RecordingController(Controller):

  def __init__(self, kaicong_ip):
    Controller.__init__(self)
    self.ip = kaicong_ip
  
  def begin(self, nsecs = None):
    self.logger.error("TODO: begin recording")

  def end(self):
    self.logger.error("TODO: end recording")
