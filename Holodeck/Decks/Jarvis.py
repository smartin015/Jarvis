#!/usr/bin/env python
import logging
import threading
logging.basicConfig()
logging.addLevelName( logging.WARNING, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName( logging.ERROR, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR))

from Holodeck.Settings import Pipe as P
from serial import Serial
from Tests.TestSerial import TestSerial
from Outputs.ScreenController import ScreenController as scl
from Outputs.RGBMultiController import RGBState, NTOWER, NRING
from Holodeck.Server import HolodeckServer
import time

class Holodeck(HolodeckServer):
  def __init__(self, devices):
    self.devices = devices['livingroom']
    self.devices['proj'] = scl()

    time.sleep(2.0) # Need delay at least this long for arduino to startup
    self.devices['tower'].setState(RGBState.STATE_MANUAL)
    time.sleep(1.0)

    self.img_path = "Holodeck/Images/"
    self.last_img = None
    self.screen_transition = None
    HolodeckServer.__init__(self)

  def mainloop(self):
    t = threading.Thread(target = self.serve_forever)
    t.daemon = True
    t.start()

    self.devices['proj'].mainloop()

  def get_pipeline_handlers(self):
    return [
      ([P.WINDOWTOP, P.WINDOWBOT], self.window_leds),
      ([P.FLOOR], self.floor_leds),
      ([P.TOWER, P.RING], self.tower_ring),
      ([P.WALLIMG], self.wall_scrn),
      ([P.LIGHTS], self.lights),
    ]

  def get_pipeline_defaults(self):
    return {
      P.WINDOWTOP:  [0,0,0],
      P.WINDOWBOT:  [0,0,0],
      P.FLOOR:      [0,0,0],
      P.TOWER:      [[0,0,0]]*NTOWER,
      P.RING:       [[0,0,0]]*NRING,
      P.WALLIMG:    None,
      P.LIGHTS:     False,
    }

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

  def wall_scrn(self, scrn):
    if self.last_img != scrn:
      print "up"
      path = "%s/%s_%s_%s.jpg" % tuple([self.img_path] + scrn)
      if not self.screen_transition:
        self.transition_screen = scl.loadimg(self.last_img).copy()
        self.screen_transition = scl.gen_sweep(scl.loadimg(self.last_img), final, self.transition_screen)
      return self.handle_screen_transition(final)
    
      self.devices['proj'].set_scrn(scl.loadimg(self.cur_img))

  def trans_wall_img(self, screen):
    final = self.steady_mapping[P.WALLIMG](screen)
    if not self.screen_transition:
      self.transition_screen = screen.copy()
      self.screen_transition = scl.gen_sweep(screen, final, self.transition_screen)
    return self.handle_screen_transition(final)
    
  def trans_window_img(self, screen):
    final = self.steady_mapping[P.WINDOWIMG](screen)
    if not self.screen_transition:
      self.transition_screen = screen.copy()
      self.screen_transition = scl.gen_zoom(screen, final, self.transition_screen)
    return self.handle_screen_transition(final)
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

  def handle_screen_transition(self, final):
    try:
      self.screen_transition.next()
      return self.transition_screen
    except StopIteration:
      self.handle_blacklist()
      self.remove_from_pipeline()
      self.transition = True
      self.insert_into_pipeline()
      return final


if __name__ == "__main__":
  from main import init_outputs
  devices = init_outputs()
  # TODO: Base this on arduino communication to the computer
  h = Holodeck(devices) 
  h.mainloop()

