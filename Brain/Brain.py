from JarvisBase import JarvisBase
from Holodeck.Decks.Jarvis import Holodeck
import time
import threading
import datetime

from Objects import *
from Modes import *

class JarvisBrain(JarvisBase):
  ABSORB_MS = 3000
  HIGH_ACTIVITY = 0.3

  def __init__(self, outputs):
    JarvisBase.__init__(self)
    self.outputs = outputs
    self.l = threading.Lock()
    self.last_command_time = datetime.datetime.now()
    self.commanded_mode = None #Used to suppress non-mode commands when mode is running
    self.logger.info("Initializing Jarvis Virtual Control Matrix")
    
    # TODO: Shift to DB
    # object name -> synonyms
    self.objectMap = {
      #'sleep': ['sleep', 'night', 'bed'],
      'lights': ['lights', 'light'],
      'projector': ['projector', 'screen'],
      'audio': ['audio', 'music'],
      'environment': ['ac'],
      'sideprojector': ['auxillary'],
      'holodeck': ['holodeck']
    }
    
    # object name -> actual object to command
    self.objects = {}
    self.objects['projector'] = Projector()
    self.objects['lights'] = MainLight()
    self.objects['environment'] = AC()
    self.objects['audio'] = Audio()
    self.objects['sideprojector'] = AuxProjector()
    self.objects['holodeck'] = HolodeckMode()

  def findTarget(self, command):
    # TODO: Flatten the mapping (word -> key, not key -> words)
    for word in command:
      for k in self.objectMap.keys():
        if word in self.objectMap[k]:
          return k
    return None

  def isValid(self, command, activity_level = 0):
    target = self.findTarget(command)

    if target is None:
      return False

    print command
    # TODO: Reenable once working properly
    #if activity_level > self.HIGH_ACTIVITY and not "please" in command:
    #  self.logger.warn("Suppressed command without 'please' in high vocal traffic")
    #  # TODO: Put a blinky thing here
    #  return False

    return self.objects[target].isValid(command)

  def timeDelta(self):
    c = datetime.datetime.now() - self.last_command_time 
    return (c.days * 24 * 60 * 60 + c.seconds) * 1000 + c.microseconds / 1000.0

  def processInput(self, command, origin):
    target = self.findTarget(command)
    #TODO: Potential concurrency issues - should really be using a lock here.
    self.l.acquire(True)
    if target and self.timeDelta() > JarvisBrain.ABSORB_MS:
      self.last_command_time = datetime.datetime.now()
      self.l.release()

      if self.commanded_mode and self.commanded_mode != target:
        self.logger.info("Suppressing command (still in mode %s)" % self.commanded_mode)
        return False

      self.logger.info("Commanding " + target)
      if hasattr(self.objects[target], "MODE"):
        args=(self.outputs, command, origin, self.objects)

        if self.commanded_mode:
          self.commanded_mode = None
        else:
          self.commanded_mode = target
      else:
        args=(self.outputs, command, origin)
      t = threading.Thread(target=self.objects[target].handle, args=args)
      t.daemon = True
      t.start()
      return True
    else:
      self.l.release()
      return False

  def update_connection_status(self, good_connection):
    if not good_connection:
      tower_default = RGBState.STATE_ERROR 
    else:
      tower_default = RGBState.STATE_FADE

    self.logger.debug("Set tower default to %d" % tower_default)
    self.outputs['tower'].setDefault(tower_default, keepalive=True)
    self.outputs['tower'].setState(tower_default)

        
if __name__ == "__main__":
  # Interactive console
  jarvis = JarvisBrain()
  
  cmd = raw_input('Your command, sir: ')
  while cmd != "":
    jarvis.processInput(None, cmd.split(" "), "console")
    cmd = raw_input('Your command, sir: ')
  
