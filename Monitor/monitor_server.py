import SocketServer
import logging
import socket
import threading
import json

UDP_PORT = 12304
PORT = 9195

class MonitorRequestHandler(SocketServer.StreamRequestHandler):
  timeout = 5
  def handle(self):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.setLevel(logging.DEBUG)
    self.logger.debug('Got connection')
    self.server.userlist.append(self.request)

    while True:
      try:
        msg = json.loads(self.request.recv(16384).strip())
        self.logger.debug("Got %s, ignoring" % str(msg))
        self.server.handle(msg['data'])
      except socket.timeout:
        if not self.server.running:
          break
        else:   
          continue
      except:
        break
    
    self.close()

  def close(self):
    if self.request in self.server.userlist:
      self.server.userlist.remove(self.request)
    self.logger.warn("Closing")
    self.request.close()

class MonitorServer(SocketServer.ThreadingTCPServer, object):
  daemon_threads = True
  allow_reuse_address = True

  def __init__(self, server_address=None):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.setLevel(logging.DEBUG)
    self.userlist = []

    if not server_address:
      server_address = (socket.gethostname(), PORT)
    
    self.logger.debug("Using address "+str(server_address))

    SocketServer.ThreadingTCPServer.__init__(self, server_address, MonitorRequestHandler)
    self.running = True
    self.logger.debug("Initialized")

  def broadcast(self, data):
    #print json.loads(data)['msg']
    print "Broadcast: %s" % (data if len(data) <= 40 else data[:37]+"...")
    for user in self.userlist:
      user.send(data+"\n")
     
if __name__ == "__main__":
  logging.basicConfig()

  srv = MonitorServer()
  print "Starting up server"
  t = threading.Thread(target = srv.serve_forever)
  t.start()
  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((socket.gethostname(), UDP_PORT))
    while True:
      # TODO: Timeouts? Count number of requests in time period
      data, addr = sock.recvfrom(4096) # buffer size is 1024 bytes
      print data
      srv.broadcast(data)
  finally:
    srv.shutdown()
    srv.server_close()
    srv.running = False
