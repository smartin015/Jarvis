import SocketServer
import logging
import socket
import threading
import json
import Queue
import traceback
import time


class RobustJSONRequestHandler(SocketServer.StreamRequestHandler):
  timeout = 5
  def handle(self):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.setLevel(logging.DEBUG)
    self.logger.debug('Got connection')
    self.server.userlist.append(self.request)

    while True:
      try:
        msg = self.request.recv(16384).strip()
        if not msg:
          self.logger.warn("Client disconnected, ending handler")
          break

        data = json.loads(msg)
        self.server.handle(data)
      except socket.timeout:
        if not self.server.running:
          self.logger.warn("Server shutdown, ending handler")
          break
        else:   
          continue
      except:
        self.logger.error(traceback.format_exc())
        self.logger.error("Unhandled exception, ending handler")
        break
    
    self.close()

  def close(self):
    if self.request in self.server.userlist:
      self.server.userlist.remove(self.request)
    self.request.close()

class RobustJSONServer(SocketServer.ThreadingTCPServer, object):
  """ JSON-based TCP server """

  daemon_threads = True
  allow_reuse_address = True

  def __init__(self, server_address):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.setLevel(logging.DEBUG)
    self.userlist = []
    self.logger.debug("Using address "+str(server_address))
    SocketServer.ThreadingTCPServer.__init__(self, server_address, RobustJSONRequestHandler)
    self.running = True
    self.logger.debug("Initialized")

    t = threading.Thread(target = self.serve_forever)
    t.daemon = True
    t.start()
    self.logger.debug("started")

  def broadcast(self, data):
    #print json.loads(data)['msg']
    msg = json.dumps(data)
    print "Broadcast: %s" % (msg if len(msg) <= 40 else msg[:37]+"...")
    for user in self.userlist:
      user.send(msg+"\n")

  def handle(self, data):
    raise Exception("Unimplemented")
  
class RobustJSONClient():
  CONNECT_TIMEOUT = 3.0
  RECONNECT_DELAY = 5.0

  def __init__(self, server_address):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.setLevel(logging.DEBUG)
    self.server_address = server_address
    self.connected = threading.Event()
    self.lock = threading.Lock()
    self.connect()

  def connect(self):
    # TODO: Robustify
    while True:
      self.logger.debug("Attempting to connect to %s..." % str(self.server_address))
      try:
        self.s = socket.create_connection(self.server_address, self.CONNECT_TIMEOUT)
        self.logger.debug("Connected to %s" % str(self.server_address))
        break
      except socket.error:
        self.logger.error(traceback.format_exc())
        self.logger.debug("Trying again in %d seconds..." % self.RECONNECT_DELAY)
        time.sleep(self.RECONNECT_DELAY)

    self.connected.set()

  def send(self, data):
    msg = json.dumps(data)
    self.connected.wait()
    self.lock.acquire()
    self.s.send(msg)
    self.lock.release()
    
  def recv(self, maxlen=65535):
    self.connected.wait()
    self.lock.acquire()
    msg = self.s.recv(maxlen)
    self.lock.release()
    return json.loads(msg)

  def sendrcv(self, data, maxlen=65535):
    self.send(data)
    return self.recv()

  def close(self):
    self.s.shutdown(socket.SHUT_RDWR) # Graceful close
    self.s.close()
    

class RobustWebsocketPassthrough():
  TIMEOUT = 1.0

  def __init__(self, ws_request, server_address):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.setLevel(logging.INFO)
    self.servers = []
    self.q = Queue.Queue()
    self.request = ws_request

    try:
      self.target = RobustJSONClient(server_address, timeout=self.TIMEOUT)
      t = threading.Thread(target=self.handle_server)
      t.daemon = True
      t.start()
      self.logger.debug("Connection to %s established" % host)
    except socket.timeout:
      self.logger.error("Connection to %s timed out" % host)
    #except:
    #  self.logger.error("Could not connect to %s:%d" % (host, port))

  def __del__(self):
    self.target.close()

  def send_to_server(self, msg):
    if not msg:
      self.logger.warning("Websocket connection closed")
      self.receiver.stop()
      self.logger.error("TODO: CLOSE TARGET SOCKET")
      return

    if not self.target:
      self.logger.error("Connection closed")
      return

    try: 
      self.target.send(msg+"\n")
    except socket.error, e:
      if isinstance(e.args, tuple) and e[0] == errno.EPIPE:
        self.logger.error("Remote \"%s\" disconnected" % (self.target.getpeername()))
      else:
        raise

    self.logger.debug("Sent %s to server" % msg)

  def handle_server(self):
    f = self.target.makefile()
    while True: #TODO: could be done better
      try:
        msg = f.readline()
        if not msg:
          self.logger.warn("Server connection closed")
          return

        self.logger.debug(((msg[:40] + '..') if len(msg) > 40 else msg))
        self.logger.debug("Adding message to queue")
        self.q.put(msg)

      except socket.timeout:
        continue
  
  def handle_print(self):
    # Use when testing, no websockets
    while True:
      try:
        msg = self.q.get(True, 5.0)
      except Queue.Empty:
        continue

      print msg

  def handle_ws(self):
    from mod_pywebsocket.msgutil import MessageReceiver
    self.receiver = MessageReceiver(self.request, self.send_to_server)
    while not self.receiver._stop_requested:
      try:
        msg = self.q.get(True, 5.0)
      except Queue.Empty:
        continue
  
      self.request.ws_stream.send_message(msg, binary=False)
      #self.logger.debug("Sent %s" % ((msg[:40] + '..') if len(msg) > 40 else msg))
      self.logger.debug("Sent %s" % msg)


if __name__ == "__main__":
  logging.basicConfig()
  logger = logging.getLogger("main")
  logger.setLevel(logging.DEBUG)

  
  server_address = (socket.gethostname(), 9996)

  logger.debug("Starting server")
  srv = RobustJSONServer(server_address)

  logger.debug("Starting client")
  cli = RobustJSONClient(server_address)

  raw_input("Enter to continue")
  logger.debug("Stopping client")
  cli.close()

  time.sleep(0.5)
  assert(len(srv.userlist) == 0)

  raw_input("Enter to continue")

  
