import socket
import SocketServer
from Holodeck.holodeck import Holodeck
from Holodeck.effects import get_all_effects
import json
import logging
from Holodeck.effects import get_all_effects
PORT = 9615
   
class HolodeckRequestHandler(SocketServer.StreamRequestHandler):
  def handle(self):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.setLevel(logging.DEBUG)
    self.logger.debug('Got connection')

    # Grab holodeck state and send to client
    self.request.send(json.dumps({"type":"init", "data": self.server.deck.get_meta()}))
  
    self.server.userlist.append(self.request)

    while True:
      try:
        msg = json.loads(self.rfile.readline().strip())
        self.logger.debug("Got %s" % str(msg))
        self.server.deck.handle(msg['data'])
      except socket.timeout:
        print "timeout"
        continue
      except:
        if self.request in self.server.userlist:
          self.server.userlist.remove(self.request)
        self.logger.warn("Closing")
        self.request.close()
        return


class HolodeckServer(SocketServer.ThreadingTCPServer):
  daemon_threads = True
  allow_reuse_address = True

  def __init__(self, server_address=None):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.setLevel(logging.DEBUG)
    self.userlist = []

    if not server_address:
      server_address = (socket.gethostname(), PORT)
    
    self.logger.debug("Using address "+str(server_address))

    SocketServer.ThreadingTCPServer.__init__(self, server_address, HolodeckRequestHandler)
    self.begin()
  
  def broadcast(self, data):
    self.logger.debug("Broadcast %s" % str(data))
    for user in self.userlist:
      user.send(data)

  def broadcast_state(self, state):
    self.broadcast(json.dumps({"type":"delta", "data":state}))

  def begin(self):
    self.deck = Holodeck(
      get_all_effects(), 
      self.get_pipeline_defaults(),
      self.get_pipeline_handlers(),
      self.broadcast_state
    )
    self.deck.daemon = True
    self.deck.start()
    self.logger.debug("Holodeck started")
    
  def get_pipeline_handlers(self):
    raise Exception("Unimplemented")

  def get_pipeline_defaults(self):
    raise Exception("Unimplemented")


