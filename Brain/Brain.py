from JarvisBase import JarvisBase
import time
import threading
import datetime

from Outputs.RGBController import RGBState

class BinaryObject(JarvisBase):
  def __init__(self):
    JarvisBase.__init__(self)
    self.state = 0
  
  def isValid(self, words):
   return ('on' in words) or ('off' in words)
     
  def parse(self, room, words):
    oldState = self.state
    if 'on' in words:
      self.turnOn(room)
    elif 'off' in words:
      self.turnOff(room)
      
  def turnOff(self, room):
    self.logger.error("TODO: Implement turnOff")

  def turnOn(self, room):
    self.logger.error("TODO: Implement turnOn")

class MainLight(BinaryObject):
  def isValid(self, words):
    return True

  def parse(self, room, words):
    room['tracklight'].toggle()
    print "Toggled"
      
class Projector(BinaryObject):
  name = "Projector"
 
  def isValid(self, words):
    return True

  def parse(self, room, words):
    room['tower'].queueState(RGBState.STATE_CHASE, 1.0)
    self.play_sound("Outputs/VoiceFiles/confirm.wav")
    self.powerbtn(room)
    self.powerbtn(room)

  def powerbtn(self, room):
    room['projector'].send("/home/jarvis/Jarvis/Outputs/IRCommandFiles/ProjectorPower.txt")
    room['projector'].send("/home/jarvis/Jarvis/Outputs/IRCommandFiles/ProjectorPower.txt")


# MODE OBJECTS
class ModeObject(BinaryObject):
  def parse(self, room, words):
    self.state = not self.state
    self.updateState()
        
        
class PartyMode(ModeObject):
  name = "Party Mode"
    
        
# JARVIS CENTRAL PROCESSING
class JarvisBrain(JarvisBase):
  ABSORB_MS = 1000

  def __init__(self):
    JarvisBase.__init__(self)
    self.l = threading.Lock()
    self.last_command_time = datetime.datetime.now()
    self.logger.info("Initializing Jarvis Virtual Control Matrix")
    
    # object name -> synonyms
    self.objectMap = {
        'party': ['party', 'fiesta', 'rave'],
        'movie': ['movie', 'film', 'video', 'tv', 'television'],
        'sleep': ['sleep', 'night', 'bed'],
      'lights': ['lights', 'light', 'lighting'],
      'projector': ['projector', 'screen'],
      'music': ['music', 'song', 'audio', 'sound'],
      'environment': ['temperature', 'warm', 'hot', 'cool', 'cold', 'warmer', 'hotter', 'cooler', 'colder', 'AC', 'heater', 'fan']
    }
    
    # object name -> actual object to command
    self.objects = {}
    self.objects['projector'] = Projector()
    self.objects['party'] = PartyMode()
    self.objects['lights'] = MainLight()

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

  def processInput(self, room, command):
    target = self.findTarget(command)
    #TODO: Potential concurrency issues - should really be using a lock here.
    self.l.acquire(True)
    if target and self.timeDelta() > JarvisBrain.ABSORB_MS:
      self.last_command_time = datetime.datetime.now()
      self.l.release()
      self.logger.info("Commanding " + target)
      t = threading.Thread(target=self.objects[target].parse, args=(room, command))
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
  
