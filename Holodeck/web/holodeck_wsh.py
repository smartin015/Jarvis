# Copyright 2011, Google Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import json
import logging
import threading
import Queue
import socket
import logging

from mod_pywebsocket.msgutil import MessageReceiver
from Holodeck.Engine import classname_to_id
from Holodeck.Server import HolodeckServer, PORT
from Holodeck.Settings import SERVER_LIST


class HolodeckController():
  TIMEOUT = 1.0

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

      # Create this tab if not already made
      if not icon_meta.get(meta['tab'], None):
        icon_meta[meta['tab']] = {}
      icon_meta[meta['tab']][meta['id']] = meta 

    return icon_meta

  def deck_broadcast(self, cmd_json):
    if not cmd_json:
      self.logger.warning("Websocket connection closed")
      self.receiver.stop()
      self.logger.error("TODO: CLOSE TARGET SOCKETS")
      return

    for s in self.servers:
      if not s:
        self.logger.debug("Connection not open, skipping...")
        continue
      s.send(cmd_json+"\n")

    self.logger.debug("Sent %s to all decks" % cmd_json)

  def handle_deck(self, deck):
    while True: #TODO: could be done better
      try:
        msg = deck.recv(2048)
        if not msg:
          self.logger.warn("Deck connection closed")
          return

        self.logger.debug("Got %s" % ((msg[:40] + '..') if len(msg) > 40 else msg))

        if deck is not self.servers[0]: # First to connect is host
          self.logger.debug("Non-host message, ignoring.")
          continue

        self.logger.debug("Adding message to queue")
        self.q.put(msg)
      except socket.timeout:
        continue
  
  def handle_ws(self):
    self.receiver = MessageReceiver(self.request, self.deck_broadcast)
    init_received = False
    while not self.receiver._stop_requested:
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



def web_socket_do_extra_handshake(request):
    # This example handler accepts any request. See origin_check_wsh.py for how
    # to reject access from untrusted scripts based on origin value.
    pass  # Always accept.


def web_socket_transfer_data(request):
  con = HolodeckController(request, SERVER_LIST)
  con.handle_ws()

    
      
