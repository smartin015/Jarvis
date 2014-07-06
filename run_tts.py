#!/usr/bin/env python
import config
import gobject
from Inputs.TTSServer import TTSServer
import logging
from Inputs.source_discovery import get_sources
import socket
import pygst
pygst.require('0.10')
import gst
import threading


LM_PATH = "/home/jarvis/Jarvis/Brain/commands.lm"
DICT_PATH = "/home/jarvis/Jarvis/Brain/commands.dic"

def path_to_name(path):
  for i in config.TTS:
    if config.TTS[i]['device'] == path:
      return i
  return None

if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  gobject.threads_init()
  sources = get_sources()

  logging.info("Discovered sources:")
  mics = {}
  for src_id in sources:
    source = sources[src_id]
    name = path_to_name(source['path'])
    if not name:
      logging.error(
        "UNUSED\t(%d) %s %s" % (
          source['id'], source['name'], source['path']
        )
      )
    else:
      port = config.TTS[name]['port']
      host = config.TTS[name]['host']
      logging.info(
        "%s\t(%d) %s:%d" % (name, source['id'], host, port)
      )
      mics[name] = {"port": port, "host": host, "source_id": source['id']}

  # TODO: Indicate missing input devices
  # TODO: Probably want to do this per-process eventually
  logging.info("Starting up audio servers")
  servers = {}
  for (name, mic) in mics.items():
    src = gst.element_factory_make("pulsesrc", "src")
    src.set_property("device", mic['source_id'])
    srv = TTSServer(name, (mic['host'], mic['port']), src, LM_PATH, DICT_PATH)
    t = threading.Thread(target = srv.serve_forever)
    t.daemon = True
    t.start()
    servers[name] = srv
  

  import threading
  # This loops the program until Ctrl+C is pressed
  g_loop = threading.Thread(target=gobject.MainLoop().run)
  g_loop.daemon = True
  g_loop.start()
  logging.info("Audio servers started")




  raw_input("Enter to exit")

      
      


  
