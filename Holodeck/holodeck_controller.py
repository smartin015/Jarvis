from Holodeck.effects import get_all_effects
from Holodeck.pipe import Pipe as P
from Holodeck.holodeck import Holodeck
from serial import Serial
from Tests.TestSerial import TestSerial
from Outputs.RelayController import RelayController
from Outputs.RGBSingleController import RGBSingleController
from Outputs.RGBMultiController import RGBMultiController, RGBState, NTOWER, NRING
from Outputs.IRController import IRController
from Outputs.ScreenController import ScreenController
from Outputs.AudioController import AudioController
import socket
import time
import json

PORT = 9604
    
class HolodeckServer():
  def get_pipeline_handlers(self):
    raise Exception("Unimplemented")

  def get_pipeline_defaults(self):
    raise Exception("Unimplemented")

  def begin(self):
    # Start up the holodeck
    self.deck = Holodeck(
      get_all_effects(), 
      self.get_pipeline_defaults(),
      self.get_pipeline_handlers()
    )
    self.deck.daemon = True
    self.deck.start()

  def handle(self, data):
    self.deck.handle(data)
 
  def serve_forever(self, host=None, port=PORT):
    self.begin()

    if not host:
      host = socket.gethostname()
    self.s = socket.socket()         
    self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.s.bind((host, port))        
    self.s.listen(5)                 

    while True:
      c, addr = self.s.accept()    

      print 'Got connection from', addr

      msg = json.loads(c.recv(1024))
      response = self.deck.handle(msg['data'])
      print "Sending", response
      c.send(json.dumps({"type":"delta", "data": response}))
      c.close()      

    
class HolodeckController():
  TIMEOUT = 0.1
  def __init__(self, host=None, port=PORT):
    if host:
      self.host = host  
    else:
      self.host = socket.gethostname()
    self.port = port

  def send_cmd_json(self, cmd_json):
    try:
      s = socket.create_connection((self.host, self.port), timeout=self.TIMEOUT)
      s.send(cmd_json)
      result = s.recv(1024)
      s.close()
      return result
    except socket.timeout:
      print "Connection %s timed out" % self.host
      return None

  def send_cmd(self, cmd):
    self.send_cmd_json(json.dumps(cmd))


class JarvisHolodeck(HolodeckServer):
  def __init__(self):
    
    self.devices = {
      "window": RGBSingleController(Serial("/dev/ttyUSB4", 9600)),
      "couch": RGBSingleController(Serial("/dev/ttyUSB3", 9600)),
      "tower": RGBMultiController(Serial("/dev/ttyACM0", 115200)),
      "proj_wall": ScreenController(socket.gethostname(), imgpath="Assets/Images/"),
      "lights": RelayController(Serial("/dev/ttyUSB5", 9600)),
    }

    time.sleep(2.5) # Need delay at least this long for arduino to startup
    self.devices['tower'].setState(RGBState.STATE_MANUAL)
    time.sleep(1.0)

  def get_pipeline_handlers(self):
    return [
      ([P.WINDOWTOP, P.WINDOWBOT], self.window_leds),
      ([P.FLOOR], self.floor_leds),
      ([P.TOWER, P.RING], self.tower_ring),
      ([P.WALLIMG], self.wall_img),
      ([P.LIGHTS], self.lights),
    ]

  def get_pipeline_defaults(self):
    return {
      P.WINDOWTOP:  [0,0,0],
      P.WINDOWBOT:  [0,0,0],
      P.FLOOR:      [0,0,0],
      P.TOWER:      [[0,0,0]]*NTOWER,
      P.RING:       [[0,0,0]]*NRING,
      P.WALLIMG:    None,
      P.LIGHTS:     False,
    }

  def window_leds(self, top, bot):
    self.devices['window'].write(top, bot)  

  def floor_leds(self, rgb):
    self.devices['couch'].write(rgb)
  
  def tower_ring(self, trgb, rrgb):
    for (i,c) in enumerate(trgb+rrgb):
      self.devices['tower'].manual_write(i, c)
    self.devices['tower'].manual_update()

  def wall_img(self, img):
    self.devices['proj_wall'].slide_to(img)

  def lights(self, is_on):
    self.devices['lights'].set_state(is_on)
  

class ToddHolodeck(HolodeckServer):
  def __init__(self):
    
    self.devices = {
      "proj_window": ScreenController(socket.gethostname()),
      "audio": AudioController(socket.gethostname()),
    }
    self.last_sounds = []

  def get_pipeline_handlers(self):
    return [
      ([P.WINDOWTOP, P.WINDOWBOT], self.window_leds),
      ([P.FLOOR], self.floor_leds),
      ([P.TOWER, P.RING], self.tower_ring),
      ([P.WINDOWIMG], self.window_img),
      ([P.WALLIMG], self.wall_img),
      ([P.LIGHTS], self.lights),
      ([P.SOUND], self.sound),
    ]

  def get_pipeline_defaults(self):
    return {
      P.WINDOWTOP:  [0,0,0],
      P.WINDOWBOT:  [0,0,0],
      P.FLOOR:      [0,0,0],
      P.TOWER:      [[0,0,0]]*NTOWER,
      P.RING:       [[0,0,0]]*NRING,
      P.WINDOWIMG:  None,
      P.WALLIMG:    None,
      P.LIGHTS:     False,
      P.SOUND:      [], 
      P.TEMP:       None,
    }

  def window_img(self, img):
    self.devices['proj_window'].zoom_to(img)
  
  def sound(self, sounds=[]):
    for s in sounds:
      if s not in self.last_sounds:
        self.devices['audio'].play(s)
    for s in self.last_sounds:
      if s not in sounds:
        self.devices['audio'].fade_out(s)
    self.last_sounds = sounds


if __name__ == "__main__":
  deck = JarvisHolodeck()
  deck.begin()

  # Test to see what the deck does
  print deck.handle({'lightning': True})

  raw_input("Enter to exit:")

