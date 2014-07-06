#!/usr/bin/env python
import gobject
from Inputs.TTSServer import TTSServer
import logging
from Inputs.source_discovery import get_sources
import socket
import pygst
pygst.require('0.10')
import gst

LM_PATH = "/home/jarvis/Jarvis/Brain/commands.lm"
DICT_PATH = "/home/jarvis/Jarvis/Brain/commands.dic"

path_map = {
  "pci-0000:00:1d.7-usb-0:4.7.4:1.0": ("desklapel", 9000),
  "pci-0000:00:1d.7-usb-0:4.6:1.0": ("livingroom", 9001),
  "pci-0000:00:1d.7-usb-0:4.5:1.0": ("hackspace", 9002),
}

host = socket.gethostname()

if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  gobject.threads_init()
  sources = get_sources()

  logging.info("Discovered sources:")
  mics = {}
  for src_id in sources:
    source = sources[src_id]
    (name, port) = path_map.get(source['path'], (None, None))
    if not name or not port:
      logging.info(
        "UNUSED\t(%d) %s %s" % (
          source['id'], source['name'], source['path']
        )
      )
    else:
      logging.info(
        "%s\t(%d) %s:%d" % (name, source['id'], host, port)
      )
      mics[name] = {"port": port, "host": host, "source_id": source['id']}

  # TODO: Probably want to do this per-process eventually
  logging.info("Starting up audio servers")
  servers = {}
  for (name, mic) in mics.items():
    src = gst.element_factory_make("pulsesrc", "src")
    src.set_property("device", mic['source_id'])
    srv = TTSServer((mic['host'], mic['port']), src, LM_PATH, DICT_PATH)
    servers[name] = srv
  
  import threading
  # This loops the program until Ctrl+C is pressed
  g_loop = threading.Thread(target=gobject.MainLoop().run)
  g_loop.daemon = True
  g_loop.start()
  logging.info("Audio servers started")

  raw_input("Enter to exit")

      
      


  
