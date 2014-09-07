from Objects import CommandObject
from Remote.remote_client import send_remote_cmd
from Holodeck.Decks.Jarvis import Holodeck
import threading

class ModeObject(CommandObject):
  MODE = True # Jarvis checks this to see if should send object list to parse()

  STARTING_STATE = {
  }

  def __init__(self):
    CommandObject.__init__(self)
    self.mode_on = False
    self.saved_state = None

  def modethread(self, *args):
    self.setup(*args)
    self.logger.debug("Entering run state")
    self.run(*args)
    self.teardown(*args)
    self.logger.debug("Mode ended")

  def setup(self, outputs, words, origin, objects):
    self.logger.debug("Setting up")
    self.saved_state = dict([(k,objects[k].getState()) for k in self.STARTING_STATE.keys()])
    self.logger.debug("Saved state: %s" % str(self.saved_state))
    for (k, v) in self.STARTING_STATE.items():
      objects[k].setState(v, outputs, words, origin)

  def teardown(self, outputs, words, origin, objects):
    self.logger.debug("Tearing down")
    for (k, v) in self.saved_state.items():
      self.logger.debug("Setting object %s state to %s" % (k, v))
      objects[k].setState(v, outputs, words, origin)

  def parse(self, outputs, words, origin, objects):
    if self.mode_on:
      self.mode_on = False
      self.logger.info("Stopping")
    else:
      self.mode_on = True
      self.logger.info("Starting")
      t = threading.Thread(target = self.modethread, args=(outputs, words, origin, objects))
      t.daemon = True
      t.start()

  def run(self, outputs, words, origin, objects):
    while self.mode_on:
      raise Exception("TODO: Implement")
        
class HolodeckMode(ModeObject):
  STARTING_STATE = {
    "projector": "on",
    "sideprojector": "on",
    "lights": "off",
  }

  def run(self, outputs, words, origin, objects):

   # Start holodeck on Jarvis
   h = Holodeck(outputs)
   h.setup()

   # Start holodeck on Scott PC
   send_remote_cmd("TheMothership", "audio", "Remote/setaudio.py speaker")
   send_remote_cmd("TheMothership", "holodeck", "run_holodeck.py Scott")

   while self.mode_on:
     h.update()

   h.shutdown()

   send_remote_cmd("TheMothership", "holodeck", "QUIT")
   send_remote_cmd("TheMothership", "audio", "QUIT")
   

