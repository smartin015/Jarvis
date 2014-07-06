import pygst
pygst.require('0.10')
import gst
import SocketServer
import logging
import socket
from Queue import Queue

class TTSRequestHandler(SocketServer.StreamRequestHandler):
  def handle(self):
    self.logger = logging.getLogger("TTS:")
    self.logger.setLevel(logging.DEBUG)
    self.logger.debug('Got connection')
    self.q = Queue()
    self.server.userlist.append(self.q)
    try:
      while True:
        s = self.q.get()
        self.request.send(s+"\n")
        self.logger.debug("Sent "+s)
    except:
      if self.request in self.server.userlist:
        self.server.userlist.remove(self.request)
      self.logger.warn("Closing")
      self.request.close()

class TTSServer(SocketServer.ThreadingTCPServer):
  daemon_threads = True
  allow_reuse_address = True

  def __init__(self, name, server_address, audiosrc, lm_path, dict_path):
    self.logger = logging.getLogger(name)
    self.logger.setLevel(logging.DEBUG)
    self.userlist = []

    if not server_address:
      server_address = (socket.gethostname(), port) 
    
    self.logger.debug("Using address "+str(server_address))

    SocketServer.ThreadingTCPServer.__init__(self, server_address, TTSRequestHandler)

    self.logger.info("Creating audio pipeline")
    pipeline = gst.Pipeline()

    conv = gst.element_factory_make("audioconvert", "audioconv")
    #conv.set_property("noise-shaping", 4)

    cheb = gst.element_factory_make("audiocheblimit")
    cheb.set_property("mode", "high-pass")
    cheb.set_property("cutoff", 200)
    cheb.set_property("poles", 4)
  
    cheb2 = gst.element_factory_make("audiocheblimit")
    cheb2.set_property("mode", "low-pass")
    cheb2.set_property("cutoff", 2500)
    cheb2.set_property("poles", 4)

    amp = gst.element_factory_make("audioamplify", "audioamp")
    amp.set_property("amplification", 15)

    res = gst.element_factory_make("audioresample", "audioresamp")
    
    vader = gst.element_factory_make("vader", "vad")
    vader.set_property("auto-threshold", True)
    
    asr = gst.element_factory_make("pocketsphinx", "asr")
    asr.connect('partial_result', self.asr_partial_result)
    asr.connect('result', self.asr_result)
    
    # Set the language model and dictionary.
    if lm_path and dict_path:
      asr.set_property('lm', lm_path)
      asr.set_property('dict', dict_path)

    # Now tell gstreamer and pocketsphinx to start converting speech!
    asr.set_property('configured', True)
    
    sink = gst.element_factory_make("fakesink", "fs")
    
    pipeline.add(audiosrc, conv, cheb, cheb2, amp, res, vader, asr, sink)
    gst.element_link_many(audiosrc, conv, amp, res, vader, asr, sink)
    pipeline.set_state(gst.STATE_PLAYING)
    
  def asr_partial_result(self, asr, text, uttid):
    """ This function is called when pocketsphinx gets a partial
        transcription of spoken audio. 
    """
    # TODO: Send activity to the brain
    self.logger.debug("%sP: %s" % (uttid, text))
    
  def asr_result(self, asr, text, uttid):
    """ This function is called when pocketsphinx gets a 
        full result (spoken command with a pause)
    """

    self.logger.debug(text)
    self.inject(text)

  def inject(self, text):
    for usr_queue in list(self.userlist):
      usr_queue.put(text)
    
if __name__ == "__main__":
  import gobject 
  gobject.threads_init()
  
  srv = TTSServer(
    "Test",
    None,
    gst.element_factory_make("autoaudiosrc", "asrc"), 
    None, 
    None, 
    8005
  )

  import threading
  # This loops the program until Ctrl+C is pressed
  g_loop = threading.Thread(target=gobject.MainLoop().run)
  g_loop.daemon = True
  g_loop.start()
  self.logger.debug("Audio server started")

  raw_input("Enter to exit")

  

