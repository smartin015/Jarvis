import json
import logging
import threading
import Queue
import socket

from mod_pywebsocket.msgutil import MessageReceiver
from Holodeck.holodeck import classname_to_id
from Holodeck.holodeck_server import HolodeckServer, PORT

class HolodeckController():
  TIMEOUT = 5.0

  def __init__(self, ws_request, server_list, port=PORT):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.setLevel(logging.DEBUG)
    self.servers = []
    self.q = Queue.Queue()
    self.request = ws_request

    for host in server_list:
      try:
        s = socket.create_connection((host,port), timeout=self.TIMEOUT)
        self.servers.append(s)
        t = threading.Thread(target=self.handle_deck, args=(s,))
        t.daemon = True
        t.start()
        self.logger.debug("Connection to %s established" % host)
      except socket.timeout:
        self.logger.error("Connection to %s timed out" % host)
      except:
        self.logger.error("Could not connect to %s" % host)
        continue

  def __del__(self):
    for s in self.servers:
      s.close()

  def get_meta(self):
    effect_list = get_all_effects()
    
    icon_meta = {}
    for (ename, eclass) in effect_list.items():
      meta = eclass.get_meta()
      #TODO: Show active state
      #meta['active'] = deck.is_active(meta['id'])
      meta['active'] = False

      # Create this tab if not already made
      if not icon_meta.get(meta['tab'], None):
        icon_meta[meta['tab']] = {}
      icon_meta[meta['tab']][meta['id']] = meta 

    return icon_meta

  def deck_broadcast(self, cmd_json):

    for s in self.servers:
      if not s:
        self.logger.debug("Connection not open, skipping...")
        continue
      s.send(cmd_json+"\n")

    self.logger.debug("Sent %s to all decks" % cmd_json)

  def get_response(self):
    return {"day": False}

  def handle_deck(self, deck):
    while True: #TODO: could be done better
      try:
        msg = deck.recv(2048)
        if not msg:
          self.logger.warn("Deck connection closed")
          return

        self.logger.debug("Got %s" % ((msg[:40] + '..') if len(msg) > 40 else msg))
        self.q.put(msg)
      except socket.timeout:
        continue
  
  def handle_ws(self):
    rcvr = MessageReceiver(self.request, self.deck_broadcast)
    init_received = False
    while not rcvr._stop_requested:
      try:
        msg = self.q.get(True, 5.0)
      except Queue.Empty:
        continue
  
      if json.loads(msg).get("type") == "init":
        if init_received:
          self.logger.debug("Ignoring duplicate init")
          continue
        else:
          init_received = True


      self.request.ws_stream.send_message(msg, binary=False)
      self.logger.debug("Sent %s" % ((msg[:40] + '..') if len(msg) > 40 else msg))


if __name__ == "__main__":
  #import logging
  #logging.basicConfig()
  #deck = JarvisHolodeck()

  # Test to see what the deck does
  print deck.handle({'day': True})

  raw_input("Enter to exit:")

