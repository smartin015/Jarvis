from JarvisBase import JarvisBase
from Holodeck.Decks.Jarvis import Holodeck
import threading

class ModeObject(JarvisBase):
  def __init__(self):
    JarvisBase.__init__(self)
    self.mode_on = False

  def isValid(self, words):
    return True

  def parse(self, outputs, words):
    if self.mode_on:
      self.mode_on = False
      self.logger.info("Stopping")
    else:
      self.mode_on = True
      self.logger.info("Starting")
      t = threading.Thread(target = self.run, args=(outputs,))
      t.daemon = True
      t.start()

  def run(self, outputs):
    while self.mode_on:
      raise Exception("TODO: Implement")

class PartyMode(ModeObject):

    #self.play_sound("Outputs/VoiceFiles/confirm.wav")
  def run(self, outputs):
    lr = outputs['livingroom']
    import random
    self.play_sound("mariachi.wav")

    while self.mode_on:
      cols = [random.randint(0, 255) for i in xrange(3)]
      cols2 = [random.randint(0, 255) for i in xrange(3)]
      lr['windowlight'].write(cols, cols2)
  
      cols3 = [random.randint(0, 255) for i in xrange(3)]
      lr['couchlight'].write(cols3)
      time.sleep(0.1)

    # Turn things off
    lr['windowlight'].clear()
    lr['couchlight'].clear()

        
class HolodeckMode(ModeObject):

  def run(self, outputs):
   # Start holodeck on Jarvis
   h = Holodeck(outputs)
   h.setup()

   # TODO: Start holodeck on Scott PC

   while self.mode_on:
     h.update()

   h.shutdown()
   self.logger.debug("Stopped")
   

