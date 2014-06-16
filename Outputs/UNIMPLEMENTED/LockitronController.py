from Outputs.Controller import Controller

class LockitronController(Controller):
  def __init__(self):
    Controller.__init__(self)
    self.logger.error("TODO: Init lockitron connection")
    
  def lock(self):
    self.logger.error("TODO: lock door")
    
  def unlock(self):
    self.logger.error("TODO: unlock door")
