from JarvisBase import JarvisBase

class BinaryObject(JarvisBase):
  def __init__(self):
    JarvisBase.__init__(self)
    self.state = 0
    self.turnOff() # On init, resets everything to off (since can't guess current state)
      
  def parse(self, room, input):
    oldState = self.state
    if 'on' in input:
      self.state = 1
    elif 'off' in input:
      self.state = 0
    
    # Only run change state if state has changed
    if self.state != oldState:
      self.updateState()
      
  def updateState(self):
    self.logger.info("Default updateState called for " + self.name)
    if self.state:
      self.turnOn()
    else:
      self.turnOff()
      
  def turnOn(self):
    self.logger.error("TODO (ON) for " + self.name)
      
  def turnOff(self):
    self.logger.error("TODO (OFF) for " + self.name)


class Projector(BinaryObject):
  name = "Projector"
      
  def updateState(self):
    if self.state:
      self.turnOn()
    else:
      self.turnOff()
    

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
        'movie': ['movie', 'film', 'video', 'tv'] ,
      'lights': ['lights', 'light', 'lighting'],
      'projector': ['projector', 'screen'],
      'music': ['music', 'song', 'audio', 'sound'],
      'environment': ['warm', 'hot', 'cool', 'cold', 'warmer', 'hotter', 'cooler', 'colder', 'AC', 'heater', 'fan']
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
    # TODO if no command detected, keep listening?

        
if __name__ == "__main__":
  # Interactive console
  jarvis = JarvisBrain()
  
  cmd = raw_input('Your command, sir: ')
  while cmd != "":
    jarvis.processInput(None, cmd.split(" "))
    cmd = raw_input('Your command, sir: ')
  
