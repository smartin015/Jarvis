#!/usr/bin/env python
""" Acapela Src """
# Acquired from http://lists.freedesktop.org/archives/gstreamer-devel/2012-January/034578.html

import gobject
gobject.threads_init()

import pygst
pygst.require('0.10')
import gst

import math, numpy, struct

class acapela_src(gst.BaseSrc):

    __gstdetails__ = (
        "Acapela src plugin",
        "acapela_src.py",
        "Source element that creates sound from text",
        "Glenn Pierce <glennpierce at gmail.com>")

    _src_template = gst.PadTemplate ("src",
                                     gst.PAD_SRC,
                                     gst.PAD_ALWAYS,
                                     gst.caps_new_any ())

    __gsttemplates__ = (_src_template,)

    def __init__ (self, *args, **kwargs):
        gst.BaseSrc.__init__(self)
        gst.info('creating acapela src pad')
        self.src_pad = gst.Pad (self._src_template)
        self.src_pad.use_fixed_caps()

    def do_create(self, offset, length):

        values = [int(math.sin(a)*32767) for a in numpy.arange(0.0, 12*math.pi, 0.06)]
        data = struct.pack('<' + 'h'*len(values), *values)
        buf = gst.Buffer(data)
        caps = gst.caps_from_string('audio/x-raw-int, rate=44100, endianness=1234, channels=1, width=16, depth=16, signed=true')
        buf.set_caps(caps)
        print "do_create", offset, length
        #buf.timestamp = 0 * gst.SECOND
        #buf.duration = 10 * gst.SECOND
        return gst.FLOW_OK, buf



# Register element class
gobject.type_register(acapela_src)
gst.element_register(acapela_src, 'acapelasrc', gst.RANK_MARGINAL)


if __name__ == "__main__":

  pipeline_str = 'acapelasrc ! audioconvert ! audioresample ! autoaudiosink'
  pipeline = gst.parse_launch(pipeline_str)
  pipeline.set_state(gst.STATE_PLAYING)

  main_loop = gobject.MainLoop()
  main_loop.run()
