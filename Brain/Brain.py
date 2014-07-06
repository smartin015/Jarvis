from JarvisBase import JarvisBase
from Holodeck.Decks.Jarvis import Holodeck
import time
import threading
import datetime

from Outputs.RGBMultiController import RGBState

class BinaryObject(JarvisBase):
  def __init__(self):
    JarvisBase.__init__(self)
    self.state = 0
  
  def isValid(self, words):
   return ('on' in words) or ('off' in words)
     
  def parse(self, outputs, words):
    if not self.state:
      self.turnOn(outputs)
      self.state = 1
    else:
      self.turnOff(outputs)
      self.state = 0
      
  def turnOff(self, outputs):
    self.logger.error("TODO: Implement turnOff")

  def turnOn(self, outputs):
    self.logger.error("TODO: Implement turnOn")

class AC(BinaryObject):
  def isValid(self, words):
    return True

  def parse(self, outputs, words):
    rf = outputs['livingroom']['RF']
    rf.send_IR("AirConditionerPower.txt")
    self.logger.debug("Toggled")

class MainLight(BinaryObject):
  def isValid(self, words):
    return True

  def parse(self, outputs, words):
    outputs['livingroom']['tower'].setState(RGBState.STATE_CHASE)
    outputs['livingroom']['tracklight'].toggle()
    self.play_sound("confirm.wav")
    time.sleep(1.0)
    self.logger.debug("Toggled")
    outputs['livingroom']['tower'].defaultState()
      
class Projector(BinaryObject):
  name = "Projector"

  def isValid(self, words):
    return True

  def parse(self, outputs, words):
    outputs['livingroom']['tower'].setState(RGBState.STATE_CHASE)
    self.play_sound("confirm.wav")

    rf = outputs['livingroom']['RF']

    if "screen" in words:
      # Just do screen, not projector
      if not self.state:
        self.screendown(rf)
      else:
        self.screenup(rf)
    else:
      if not self.state:
        self.turnOn(rf)
      else:
        self.turnOff(rf)
    self.state = 1 - self.state

    outputs['livingroom']['tower'].defaultState()


  def turnOn(self, rf):
    self.logger.info("Pressing power button")
    self.powerbtn(rf)
    self.logger.info("Lowering screen")
    self.screendown(rf)
    self.logger.info("Done")

  def turnOff(self, rf):
    self.logger.info("Pressing power button")
    self.powerbtn(rf)
    self.logger.info("Raising screen")
    self.screenup(rf)
    self.logger.info("Done")

  def screenup(self, rf):
    rf.send_IR("ProjectorScreenStop.txt")
    rf.send_IR("ProjectorScreenUp.txt")

  def screendown(self, rf):
    rf.send_IR("ProjectorScreenStop.txt")
    rf.send_IR("ProjectorScreenDown.txt")

  def powerbtn(self, rf):
    rf.send_IR("ProjectorPower.txt")
    rf.send_IR("ProjectorPower.txt")


# MODE OBJECTS
class ModeObject(BinaryObject):
  def parse(self, outputs, words):
    self.state = not self.state
    self.updateState()
       

class PartyMode(BinaryObject):

  def __init__(self):
    BinaryObject.__init__(self)
    self.partying = False

  def isValid(self, words):
    return True

  def parse(self, outputs, words):
    if self.partying:
      self.partying = False
      print "Stopping the party :("
      return

    print "Partying..."
    self.partying = True
    t = threading.Thread(target=self.party, args=(outputs,))
    t.start()

    #self.play_sound("Outputs/VoiceFiles/confirm.wav")
  def party(self, outputs):
    lr = outputs['livingroom']
    import random
    self.play_sound("mariachi.wav")

    while self.partying:
      cols = [random.randint(0, 255) for i in xrange(3)]
      cols2 = [random.randint(0, 255) for i in xrange(3)]
      lr['windowlight'].write(cols, cols2)
  
      cols3 = [random.randint(0, 255) for i in xrange(3)]
      lr['couchlight'].write(cols3)
      time.sleep(0.1)

    # Turn things off
    lr['windowlight'].clear()
    lr['couchlight'].clear()

        
        
# JARVIS CENTRAL PROCESSING
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
      'environment': ['temperature', 'warm', 'hot', 'cool', 'cold', 'warmer', 'hotter', 'cooler', 'colder', 'ac', 'heater', 'conditioner', 'fan']
    }
    
    # object name -> actual object to command
    self.objects = {}
    self.objects['projector'] = Projector()
    self.objects['party'] = PartyMode()
    self.objects['lights'] = MainLight()
    self.objects['environment'] = AC()

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
  
