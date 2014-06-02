from JarvisBase import JarvisBase
import time

class BinaryObject(JarvisBase):
  def __init__(self):
    JarvisBase.__init__(self)
    self.state = 0
      
  def parse(self, room, input):
    oldState = self.state
    if 'on' in input:
      self.turnOn(room)
    elif 'off' in input:
      self.turnOff(room)
      
  def turnOff(self, room):
    self.logger.error("TODO: Implement turnOff")

  def turnOn(self, room):
    self.logger.error("TODO: Implement turnOn")

      
class Projector(BinaryObject):
  name = "Projector"
 
  def powerbtn(self, room):
    room['projector'].send("/home/jarvis/Jarvis/Outputs/IRCommandFiles/ProjectorPower.txt")

  def turnOff(self, room):
    self.play_sound("Outputs/VoiceFiles/confirm.wav")
    self.powerbtn(room)
    self.powerbtn(room)

  def turnOn(self, room):
    self.play_sound("Outputs/VoiceFiles/confirm2.wav")
    self.powerbtn(room)


# MODE OBJECTS
class ModeObject(BinaryObject):
  def parse(self, room, input):
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

  def processInput(self, room, input):
    for word in input:
      for k in self.objectMap.keys():
        if word in self.objectMap[k]:
          self.logger.info("Commanding " + word)
          self.objects[word].parse(room, input)
          return True

    return False
        
if __name__ == "__main__":
  # Interactive console
  jarvis = JarvisBrain()
  
  cmd = raw_input('Your command, sir: ')
  while cmd != "":
    jarvis.processInput(None, cmd.split(" "))
    cmd = raw_input('Your command, sir: ')
  
