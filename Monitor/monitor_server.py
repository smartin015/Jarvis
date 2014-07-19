from monitor import ProcessMonitor
import SocketServer
import logging
import socket
import threading
import json

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
  
  def push_message(self, name, is_error, line):
    #self.logger.debug("Pushing %s %s %s" % (name, is_error, line))
    self.broadcast(json.dumps({"name": name, "iserr": is_error, "msg": line}))

  #def shutdown(self):
  #  self.logger.warn("Shutting down")
  #  #SocketServer.ThreadingTCPServer.shutdown(self)
  #  self.server_close()
  #  self.running = False
  #  self.logger.warn("Stopped")

  def broadcast(self, data):
    print data
    for user in self.userlist:
      user.send(data)
     
  def handle(self, data):
    """ Use this for testing/debugging of commands without server """
    raise Exception("Unimplemented")

if __name__ == "__main__":
  logging.basicConfig()

  srv = MonitorServer()

  #TODO: Put in DB
  MONITORS = (
    #ProcessMonitor("run_tts.py", srv.push_message),
    #ProcessMonitor("main.py", srv.push_message),
    ProcessMonitor("run_sockets.py", srv.push_message),
  )

  print "Starting process daemons"
  for mon in MONITORS:
    mon.daemon = True
    mon.start()

  print "Starting up server"
  t = threading.Thread(target = srv.serve_forever)
  t.start()
  raw_input("Enter to exit")
  srv.shutdown()
  srv.server_close()
  srv.running = False
  print "Server shut down, waiting for child processes..."
  for mon in MONITORS:
    mon.shutdown()
    mon.join()




  

  

