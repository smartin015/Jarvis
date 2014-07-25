#!/usr/bin/env python
import logging
import threading
from Holodeck.Settings import Pipe as P
from serial import Serial
from Tests.TestSerial import TestSerial
from Outputs.ScreenController import ScreenController as scl
from Outputs.RGBMultiController import RGBState, NTOWER, NRING
from Holodeck.Server import HolodeckServer
import time

class HolodeckBase(HolodeckServer):
  DEFAULT_IMG = ["", "clear", "day"]
  IMG_PATH = None
  IMG_TRANSITION = None

  def __init__(self, devices):
    self.devices = devices
    self.devices['proj'] = scl()
    self.last_img = self.DEFAULT_IMG
    self.last_img_screen = scl.get_black_image()
    self.last_sounds = ([],[])
    self.screen_transition = None
    
    self.img_trans = {
      "sweep": scl.gen_sweep,
      "zoom": scl.gen_zoom,
    }
    
    HolodeckServer.__init__(self)

  def setup(self):
    t = threading.Thread(target = self.serve_forever)
    t.daemon = True
    t.start()
    self.logger.debug("Server is running")

  def update(self):
    self.devices['proj'].update()

  def shutdown(self):
    super(HolodeckServer, self).shutdown() # Shut down things that rely on devices first

    defaults = self.get_pipeline_defaults()
    handlers = self.get_pipeline_handlers()
    for (handler, pipelist) in handlers:
      handler(*[defaults[p] for p in pipelist])

    self.devices['proj'].quit()

  def mainloop(self):
    self.devices['proj'].mainloop()

  def get_pipeline_handlers(self):
    raise Exception("Unimplemented")

  def get_pipeline_defaults(self):
    raise Exception("Unimplemented")

  def window_leds(self, top, bot):
    self.devices['windowlight'].write(top, bot)  

  def floor_leds(self, rgb):
    self.devices['couchlight'].write(rgb)
  
  def tower_ring(self, trgb, rrgb):
    for (i,c) in enumerate(trgb+rrgb):
      self.devices['tower'].manual_write(i, c)
    self.devices['tower'].manual_update()

  def lights(self, is_on):
    self.devices['tracklight'].set_state(is_on)

  def scrn(self, scrn):
    # TODO: Interrupted screen transitions would be EPIC
    if self.screen_transition is not None:
      try:
        self.screen_transition.next()
        self.devices['proj'].flip()
      except StopIteration:
        print "Transition complete"
        self.screen_transition = None
    elif self.last_img != scrn:
      if scrn[0] == self.DEFAULT_IMG[0]:  
        next_img = scl.get_black_image()
        print "Transitioning to empty screen"
      else:
        path = "%s%s_%s_%s.jpg" % tuple([self.IMG_PATH] + scrn)
        print "Transitioning to", path
        next_img = scl.loadimg(path)

      self.screen_transition = self.img_trans[self.IMG_TRANSITION](
        self.last_img_screen, 
        next_img, 
        self.devices['proj'].screen
      )
      
      self.last_img_screen = next_img
      self.last_img = list(scrn)
  
    # Manual clear of screen data
    for i in xrange(len(self.DEFAULT_IMG)):
      scrn[i] = self.DEFAULT_IMG[i]


  def linear_blend(self, i, rgb1, rgb2):
    blend_amount = min( float(i) / self.TRANSITION_TIME, 1 )
    return [(a*blend_amount) + (b*(1-blend_amount)) for (a,b) in zip(rgb2, rgb1)]

  def tween_blend(self, i, rgb1, rgb2, rgb3):
    if i < self.TRANSITION_TIME / 2:
      return self.linear_blend(2*i, rgb1, rgb2)
    else:
      return self.linear_blend(2*(i-self.TRANSITION_TIME/2), rgb2, rgb3)

  def trans_floor(self, prev):
    self.tfloor += 1
    if self.prev_window_bot:
      final = self.steady_mapping[P.FLOOR](prev)
      return self.tween_blend(self.tfloor, prev, self.prev_window_bot, final)
    else:
      return prev
  
  def trans_window_top(self, prev):
    self.ttop += 1
    final = self.steady_mapping[P.WINDOWTOP](prev)
    return self.linear_blend(self.ttop, prev, final)
    
  def trans_window_bot(self, prev):
    self.tbot += 1
    mid = self.steady_mapping[P.FLOOR](prev)
    final = self.steady_mapping[P.WINDOWBOT](prev)
    if not self.prev_window_bot:
      self.prev_window_bot = final
    return self.tween_blend(self.tbot, prev, mid, final)

  def sound(self, sounds):
    (ambient, effects) = sounds
    (last_ambient, last_effects) = self.last_sounds

    for s in effects:
      if s not in last_effects:
        print "playing", s
        self.devices['audio'].play(s)
        
    for s in ambient:
      if s not in last_ambient:
        print "fading in", s
        self.devices['audio'].fadein(s)
        
    for s in last_ambient:
      if s not in ambient:
        print "fading out", s
        self.devices['audio'].fadeout(s)
        
    for s in last_effects:
      if s not in effects:
        print "stopping", s
        self.devices['audio'].fadeout_fast(s)
        
    # Do list-copy to prevent getting just a reference    
    self.last_sounds = (list(ambient), list(effects))
    
    # Clear the sound array for the next pass through
    del ambient[:]
    del effects[:]
