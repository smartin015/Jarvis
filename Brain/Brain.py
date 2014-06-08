from JarvisBase import JarvisBase
import time
import threading

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
  def __init__(self):
    JarvisBase.__init__(self)
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

  def findTarget(self, command):
    # TODO: Flatten the mapping (word -> key, not key -> words)
    for word in command:
      for k in self.objectMap.keys():
        if word in self.objectMap[k]:
          return word
    return None

  def isValid(self, command):
    target = self.findTarget(command)
    return (target is not None and self.objects[target].isValid(command))

  def processInput(self, room, command):
    target = self.findTarget(command)
    if target:
      self.logger.info("Commanding " + target)
      t = threading.Thread(target=self.objects[target].parse, args=(room, command))
      t.daemon = True
      t.start()
      return True
    else:
      return False
        
if __name__ == "__main__":
  # Interactive console
  jarvis = JarvisBrain()
  
  cmd = raw_input('Your command, sir: ')
  while cmd != "":
    jarvis.processInput(None, cmd.split(" "))
    cmd = raw_input('Your command, sir: ')
  
