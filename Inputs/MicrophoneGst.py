#!/usr/bin/env python
# Origin: http://cgit.freedesktop.org/gstreamer/gst-python/tree/examples/filesrc.py

import pygst
pygst.require('0.10')
import gst

import gobject

from KaicongAudio import KaicongAudio

class MicrophoneSource(gst.BaseSrc):
    __gstdetails__ = (
        "Kaicong Audio src plugin",
        "KaicongAudioGst.py",
        "Source element that rips sound from a Kaicong IP camera",
        "Scott Martin (github: smartin015)"
    )

    _src_template = gst.PadTemplate("src",
                          gst.PAD_SRC,
                          gst.PAD_ALWAYS,
                          gst.caps_new_any()
                    )

    __gsignals__ = {
      'packet_received' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ())
    }  

    __gsttemplates__ = (_src_template,)

    def __init__(self, *args, **kwargs):
        self.caps = gst.caps_from_string('audio/x-raw-int, rate=7600, endianness=1234, channels=1, width=16, depth=16, signed=true')
        gst.BaseSrc.__init__(self)
        gst.info("Creating Kaicong src pad")
        self.src_pad = gst.Pad(self._src_template)
        self.src_pad.use_fixed_caps()

    def set_property(self, name, value):
        if name == 'ip':
            self.ip = value
        elif name == 'user':
            self.user = value
        elif name == "pwd":
            self.pwd = value
        elif name == "on" and value:
            self.audio = KaicongAudio(self.ip, user=self.user, pwd=self.pwd)
            self.audio.connect()
            gst.info("Connected audio")

    def do_create(self, offset, size):
        self.emit("packet_received")
        assert self.audio
        data = self.audio.read()
        buf = gst.Buffer(data)
        buf.set_caps(self.caps)
        print "do_create", len(buf)
        return gst.FLOW_OK, buf
        


if __name__ == "__main__":
  import gobject 
  gobject.threads_init()

  pipeline = gst.Pipeline("pipe")

  src = gst.element_factory_make("autoaudiosrc", "audiosrc")
  conv = gst.element_factory_make("audioconvert", "audioconv")
  conv.set_property("noise-shaping", 4)
  cheb = gst.element_factory_make("audiocheblimit")
  cheb.set_property("mode", "high-pass")
  cheb.set_property("cutoff", 200)
  cheb.set_property("poles", 4)

  cheb2 = gst.element_factory_make("audiocheblimit")
  cheb2.set_property("mode", "low-pass")
  cheb2.set_property("cutoff", 3000)
  cheb2.set_property("poles", 4)

  amp = gst.element_factory_make("audioamplify", "audioamp")
  amp.set_property("amplification", 25)
  res = gst.element_factory_make("audioresample", "audioresamp")
  sink = gst.element_factory_make("autoaudiosink", "audiosink")
  
  pipeline.add(src, conv, cheb, cheb2, amp, res, sink)
  gst.element_link_many(src, conv, amp, cheb, cheb2, res, sink)
  pipeline.set_state(gst.STATE_PLAYING)

  main_loop = gobject.MainLoop()
  main_loop.run()
  
