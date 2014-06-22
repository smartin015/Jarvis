import socket
import SocketServer
import json
import logging

from Holodeck.Engine import HolodeckEngine
from Holodeck.Effects import get_all_effects
from Holodeck.Settings import SERVER_PORT as PORT
   
class HolodeckRequestHandler(SocketServer.StreamRequestHandler):
  def handle(self):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.setLevel(logging.DEBUG)
    self.logger.debug('Got connection')

    # Grab holodeck state and send to client
    self.request.send(json.dumps({
      "host": self.server.server_address, 
      "type": "init", 
      "data": self.server.deck.get_meta(),
    }))
  
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
    
    self.deck = HolodeckEngine(
      get_all_effects(), 
      self.get_pipeline_defaults(),
      self.get_pipeline_handlers(),
      self.broadcast_state
    )
    self.deck.start_pipeline()
    self.logger.debug("Holodeck started")
  
  def broadcast(self, data):
    self.logger.debug("Broadcast %s" % str(data))
    for user in self.userlist:
      user.send(data)

  def broadcast_state(self, state):
    self.broadcast(json.dumps({
      "host": self.server_address,
      "type": "delta", 
      "data": state
    }))
     
  def handle(self, data):
    """ Use this for testing/debugging of commands without server """
    self.deck.handle(data)
    
  def get_pipeline_handlers(self):
    raise Exception("Unimplemented")

  def get_pipeline_defaults(self):
    raise Exception("Unimplemented")


