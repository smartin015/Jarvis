#!/usr/bin/env python
# Origin: http://cgit.freedesktop.org/gstreamer/gst-python/tree/examples/filesrc.py

import sys
import gobject 
gobject.threads_init()

import pygst
pygst.require('0.10')
import gst

from KaicongAudio import KaicongAudio


import numpy
import math
import struct

class KaicongAudioSource(gst.BaseSrc):
    __gstdetails__ = (
        "Acapela src plugin",
        "acapela_src.py",
        "Source element that creates sound from text",
        "Glenn Pierce <glennpierce at gmail.com>")

    _src_template = gst.PadTemplate("src",
                          gst.PAD_SRC,
                          gst.PAD_ALWAYS,
                          gst.caps_new_any()
                    )
  
    __gsttemplates__ = (_src_template,)

    def __init__(self, *args, **kwargs):
        gst.BaseSrc.__init__(self)
        self.audio = None
        gst.info("Creating Kaicong src pad")
        self.src_pad = gst.Pad(self._src_template)
        self.src_pad.use_fixed_caps()

        self.caps = gst.caps_from_string('audio/x-raw-int, rate=7600, endianness=1234, channels=1, width=16, depth=16, signed=true')

        # TODO: Set as property
        self.audio = KaicongAudio("192.168.1.15")
        self.audio.connect()
        gst.info("Connected audio")

    def set_property(self, name, value):
        if name == 'ip':
            self.audio = KaicongAudio(value)
            self.audio.connect()

    def do_create(self, offset, size):
        data = self.audio.read()
        buf = gst.Buffer(data)
        buf.set_caps(self.caps)
        print "do_create", len(buf)
        return gst.FLOW_OK, buf
        
        
"""
        if data:
            #return gst.FLOW_OK, gst.Buffer(np.fromstring(data, dtype=np.int16))
            values = [int(math.sin(a)*32767) for a in numpy.arange(0.0, 12*math.pi, 0.06)]
            data = struct.pack('<' + 'h'*len(values), *values)
            buf = gst.Buffer(data)
            caps = gst.caps_from_string('audio/x-raw-int, rate=8000, endianness=1234, channels=1, width=16, depth=16, signed=true')
            buf.set_caps(caps)
            print "do_create", len(data)
            return gst.FLOW_OK, buf
        else:
            # TODO: Make this actually useful?
            return gst.FLOW_UNEXPECTED, None
"""

gobject.type_register(KaicongAudioSource)
gst.element_register(KaicongAudioSource, 'asdfsrc', gst.RANK_MARGINAL)

if __name__ == "__main__":

  pipeline_str = 'asdfsrc ! audioconvert ! audioresample ! autoaudiosink'
  pipeline = gst.parse_launch(pipeline_str)
  pipeline.set_state(gst.STATE_PLAYING)

  main_loop = gobject.MainLoop()
  main_loop.run()

"""
def main(args):
    if len(args) != 2:
        print 'Usage: %s ip_addy' % (args[0])
        return -1
    
    bin = gst.Pipeline('pipeline')

    audiosrc = KaicongAudioSource('audiosource')
    assert audiosrc
    audiosrc.set_property('ip', args[1])

    caps = gst.caps_from_string('audio/x-raw-int, endianness=1234, signed=true, width=16, depth=16, rate=8000, channels=1')
    audiofilter = gst.element_factory_make("capsfilter", "filter")
    audiofilter.set_property('caps', caps)

    audiosink = gst.element_factory_make('autoaudiosink', 'sink')

    

    bin.add(audiosrc, audiofilter, audiosink)
    gst.element_link_many(audiosrc, audiofilter, audiosink)
    
    bin.set_state(gst.STATE_PLAYING);
    mainloop = gobject.MainLoop()

    def bus_event(bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            mainloop.quit()
        elif t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            mainloop.quit()           
        return True
    bin.get_bus().add_watch(bus_event)

    mainloop.run()
    bin.set_state(gst.STATE_NULL)

if __name__ == '__main__':
   sys.exit(main(sys.argv))
"""
