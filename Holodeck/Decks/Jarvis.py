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
  EMPTY_IMG = ["", "clear", "day"]

  def __init__(self, devices):
    self.devices = devices
    self.devices['proj'] = scl()

    time.sleep(2.0) # Need delay at least this long for arduino to startup
    self.devices['tower'].setState(RGBState.STATE_MANUAL)
    time.sleep(1.0)

    self.img_path = "Holodeck/Images/right/"
    self.last_img = self.EMPTY_IMG
    self.last_img_screen = scl.get_black_image()
    self.screen_transition = None
    HolodeckServer.__init__(self)

  def setup(self):
    t = threading.Thread(target = self.serve_forever)
    t.daemon = True
    t.start()

  def update(self):
    self.devices['proj'].update()

  def shutdown(self):
    super(Holodeck, self).shutdown() # Shut down things that rely on devices first

    defaults = self.get_pipeline_defaults()
    tup = self.get_pipeline_handlers()
    for i in tup :
      i[1](*[defaults[p] for p in i[0]])

    self.devices['proj'].quit()
    self.devices['tower'].manual_exit()
    

  def mainloop(self):
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
      P.WALLIMG:    list(self.EMPTY_IMG),
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
    if self.screen_transition is not None:
      try:
        self.screen_transition.next()
        self.devices['proj'].flip()
      except StopIteration:
        print "Transition complete"
        self.screen_transition = None
    elif self.last_img != scrn:
      print "Transitioning"
      if scrn == self.EMPTY_IMG:  
        self.devices['proj'].set_scrn(scl.get_black_image())
      else:
        path = "%s%s_%s_%s.jpg" % tuple([self.img_path] + scrn)
        next_img = scl.loadimg(path)
        self.screen_transition = scl.gen_sweep(
          self.last_img_screen, 
          next_img, 
          self.devices['proj'].screen
        )
        self.last_img_screen = next_img
        self.last_img = list(scrn)

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



if __name__ == "__main__":
  from run_jarvis import init_outputs
  devices = init_outputs()
  # TODO: Base this on arduino communication to the computer
  h = Holodeck(devices) 
  h.setup()
  h.mainloop()

