from JarvisBase import JarvisBase
from Holodeck.Decks.Jarvis import Holodeck
import time
import threading
import datetime

from Objects import *
from Modes import *

class JarvisBrain(JarvisBase):
  ABSORB_MS = 1000

  def __init__(self):
    JarvisBase.__init__(self)
    self.l = threading.Lock()
    self.last_command_time = datetime.datetime.now()
    self.logger.info("Initializing Jarvis Virtual Control Matrix")
    
    # TODO: Shift to DB
    # object name -> synonyms
    self.objectMap = {
      'party': ['party', 'fiesta', 'rave'],
      'movie': ['movie', 'film', 'video', 'tv', 'television'],
      'sleep': ['sleep', 'night', 'bed'],
      'lights': ['lights', 'light', 'lighting'],
      'projector': ['projector', 'screen'],
      'music': ['music', 'song', 'audio', 'sound'],
      'audio': ['audio'],
      'environment': ['ac'],
      'sideprojector': ['auxillary'],
      'holodeck': ['holodeck']
    }
    
    # object name -> actual object to command
    self.objects = {}
    self.objects['projector'] = Projector()
    self.objects['party'] = PartyMode()
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

  def isValid(self, command):
    target = self.findTarget(command)
    return (target is not None and self.objects[target].isValid(command))

  def timeDelta(self):
    c = datetime.datetime.now() - self.last_command_time 
    return (c.days * 24 * 60 * 60 + c.seconds) * 1000 + c.microseconds / 1000.0

  def processInput(self, outputs, command):
    target = self.findTarget(command)
    #TODO: Potential concurrency issues - should really be using a lock here.
    self.l.acquire(True)
    if target and self.timeDelta() > JarvisBrain.ABSORB_MS:
      self.last_command_time = datetime.datetime.now()
      self.l.release()
      self.logger.info("Commanding " + target)
      t = threading.Thread(target=self.objects[target].parse, args=(outputs, command))
      t.daemon = True
      t.start()
      return True
    else:
      self.l.release()
      return False
        
if __name__ == "__main__":
  # Interactive console
  jarvis = JarvisBrain()
  
  cmd = raw_input('Your command, sir: ')
  while cmd != "":
    jarvis.processInput(None, cmd.split(" "))
    cmd = raw_input('Your command, sir: ')
  
