#!/usr/bin/env python
import gobject
from Inputs.TTSServer import TTSServer
import logging
from Inputs.source_discovery import get_sources
import socket
import pygst
pygst.require('0.10')
import gst
import threading

from config import TTS, PATHS

def path_to_TTS(path):
  for i in TTS:
    if i.device == path:
      return i
  return None

if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  gobject.threads_init()
  sources = get_sources()

  logging.info("Discovered sources:")
  mics = {}
  for (src_id, source) in sources.items():
    tts = path_to_TTS(source['path'])
    if not tts:
      logging.error(
        "UNUSED\t(%d) %s %s" % (
          source['id'], source['name'], source['path']
        )
      )
    else:
      logging.info(
        "%s\t(%d) %s:%d" % (tts.id, source['id'], tts.host, tts.port)
      )
      mics[tts.id] = {
        "port": tts.port, 
        "host": tts.host, 
        "source_id": source['id']
      }

  # TODO: Indicate missing input devices
  # TODO: Probably want to do this per-process eventually
  logging.info("Starting up audio servers")
  servers = {}
  for (name, mic) in mics.items():
    src = gst.element_factory_make("pulsesrc", "src")
    src.set_property("device", mic['source_id'])
    srv = TTSServer(
      name, 
      (mic['host'], mic['port']), 
      src, 
      PATHS['language_model'], 
      PATHS['language_dict']
    )
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

      
      


  
