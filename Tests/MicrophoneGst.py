#!/usr/bin/env python
# Origin: http://cgit.freedesktop.org/gstreamer/gst-python/tree/examples/filesrc.py

import pygst
pygst.require('0.10')
import gst

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

