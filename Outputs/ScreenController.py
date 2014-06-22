import pygame
import pygame.locals
import os
import time
import threading
import sys

SW,SH = 1680, 1050
DELTA = 500
SCALE_DELTA = 30
VSTART = 0
IMW, IMH = SW+2*DELTA, SH+SCALE_DELTA

HSTART = -DELTA

# TODO: Thread handoff?
class ScreenController():
  def __init__(self):
    self.delta = DELTA
    self.daemon = True

    if os.name is not 'nt':
      os.environ["DISPLAY"] = ":0"
    os.environ["SDL_FBDEV"] = "/dev/fb1"
    self.screen = pygame.display.set_mode(
      (SW,SH), 
      pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
    )
    self.clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    self.clear()
  
  @classmethod
  def easeInOutQuad(self, currtime, start, delta, duration):
    currtime = float(currtime)
    start = float(start)
    delta = float(delta)
    duration = float(duration)
    currtime /= duration/2;
    # First half of easing
    if (currtime < 1): 
      return delta/2*currtime*currtime + start;

    # Second half of easing
    currtime -= 1; 
    return -delta/2 * (currtime*(currtime-2) - 1) + start;


  def mainloop(self):
    while True:
      for event in pygame.event.get():
        if (event.type == pygame.locals.QUIT or (
              event.type == pygame.locals.KEYDOWN and 
              event.key == pygame.locals.K_ESCAPE
            )):
          pygame.quit()
          return
       
      self.clock.tick(10)
      

  @classmethod
  def gen_sweep(self, img1, img2, screen):
    start = 0.0
    mid = 2.0
    overlap = 0.25
    end = 4.0
    alpha_end = 150
    delta = DELTA
    img1_start = 0
    img2_start = float(-delta)
    start_time = time.time()
    t = 0.0
    img1 = img1.convert()
    img2 = img2.convert()
    
    while t < end:
      t = time.time() - start_time
      v = ScreenController.easeInOutQuad(t, start, delta, end) 

      if t < mid+overlap:
        alpha = alpha_end * t / (mid+overlap)
        img1.set_alpha(int(alpha_end-alpha))
        screen.blit(img1,(img1_start+v,VSTART))
    
      if t > mid-overlap:
        alpha = alpha_end * (t-(mid-overlap)) / (end-(mid-overlap))  
        img2.set_alpha(int(alpha))
        screen.blit(img2,(img2_start+v,VSTART))

      yield
  
  @classmethod
  def gen_zoom(self, img1, img2, screen):
    start = 0
    mid = 2.0
    overlap = 0.25
    end = 4.0
    alpha_end = 150
    img1_start = 0
    img2_start = 0
    delta = DELTA / 8
    aspect = float(IMW)/float(IMH)
    start_time = time.time()
    t = 0.0
    img1 = img1.convert()
    img2 = img2.convert()

    img2_scaledist = end-(mid-overlap)
    im2h = int(img2.get_size()[1]-img2_scaledist)

    img2_orig = img2
    img2 = pygame.transform.smoothscale(img2, (int(aspect*im2h), im2h))

    while t < end:
      t = time.time() - start_time
      v = ScreenController.easeInOutQuad(t, start, delta, end) 

      if t < mid+overlap:
        alpha = alpha_end * t / (mid+overlap)
        img1_scale = pygame.transform.smoothscale(img1, (int(aspect*(IMH+v)), int(IMH+v)))
        img1.blit(img1_scale, (-aspect*v/2,-v/2))
        img1_scale.set_alpha((alpha_end-alpha))
        screen.blit(img1_scale,(img1_start,VSTART))
      
      if t >= mid-overlap:
        alpha = alpha_end * (t-(mid-overlap)) / (end-(mid-overlap))  
        s = t-(mid-overlap)
        img2_scale = pygame.transform.smoothscale(img2, (int(aspect*(im2h+s)), int(im2h+s)))
        img2_scale.set_alpha(alpha)
        screen.blit(img2_scale,(img2_start + (img2_scaledist-s)/2,VSTART)) #- (s-img2_scaledist)/2))

      yield
    
    img2_orig.set_alpha(alpha)
    screen.blit(img2_orig, (img2_start, VSTART))
    yield

  def set_scrn(self, scrn):
    self.screen.blit(scrn, (-self.delta, VSTART))
    pygame.display.flip()

  def flip(self):
    pygame.display.flip()

  
  def clear(self):
    self.screen.fill((0,0,0))
    pygame.display.flip()

  @classmethod
  def get_black_image(self):
    img = pygame.Surface((IMW,IMH))
    img.fill((0,0,0))
    img.set_alpha(255)
    return img

  @classmethod
  def loadimg(self, path):
    img = pygame.image.load(path).convert()
    img = pygame.transform.scale(img, (IMW,IMH))   
    return img

if __name__ == '__main__':
  con = ScreenController()
  forest = ScreenController.loadimg('Assets/Images/forest.jpg')
  grass = ScreenController.loadimg('Assets/Images/grassland.jpg')

  c = pygame.time.Clock()

  con.set_scrn(grass)
  g = ScreenController.gen_zoom(grass, forest, con.screen)
  try:
    while True:
      g.next()
      con.flip()
      c.tick(24)
  except StopIteration:
    time.sleep(2.0)
    con.set_scrn(forest)
    raw_input("Enter to continue")

  g = ScreenController.gen_zoom(forest, grass, con.screen)
  try:
    while True:
      g.next()
      con.flip()
      c.tick(24)
  except StopIteration:
    time.sleep(2.0)
    con.set_scrn(grass)
    raw_input("Enter to exit")

 
