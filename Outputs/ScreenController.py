import pygame
import os
import time
import threading

SW,SH = 1920, 1080
DELTA = 500
SCALE_DELTA = 30
VSTART = 0
IMW, IMH = SW+2*DELTA, SH+SCALE_DELTA

HSTART = -DELTA


class ScreenController(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
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
    self.daemon = True
    self.start()
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


  def run(self):
    while True:
      time.sleep(0.5)
      pygame.event.pump()

  @classmethod
  def gen_sweep(self, img1, img2, screen):
    start = 0
    mid = 50
    overlap = 10
    end = 120
    alpha_end = 150
    delta = DELTA
    img1_start = 0
    img2_start = float(-delta)

    for i in xrange(start, end):
      v = ScreenController.easeInOutQuad(i, start, delta, end) 

      if i < mid+overlap:
        alpha = i * (alpha_end/float(mid+overlap))  
        img1.set_alpha((alpha_end-alpha))
        screen.blit(img1,(img1_start+v,VSTART))
    
      if i > mid-overlap:
        alpha = (i-(mid-overlap)) * (alpha_end/float(end-(mid-overlap)))  
        img2.set_alpha(alpha)
        screen.blit(img2,(img2_start+v,VSTART))

      yield
  
  @classmethod
  def gen_zoom(self, img1, img2, screen):
    start = 0
    mid = 50
    overlap = 15
    end = 70
    alpha_end = 150
    img1_start = 0#float(-DELTA)
    img2_start = img1_start
    delta = DELTA / 8
    aspect = float(IMW)/float(IMH)
    
    img1 = img1.copy()

    img2_scaledist = end-(mid-overlap)
    im2h = img2.get_size()[1]-img2_scaledist

    img2_orig = img2
    img2 = pygame.transform.smoothscale(img2, (int(aspect*im2h), im2h))


    for i in xrange(start, end):
      v = ScreenController.easeInOutQuad(i, start, delta, end) 

      if i < mid+overlap:
        alpha = i * (alpha_end/float(mid+overlap))  
        img1_scale = pygame.transform.smoothscale(img1, (int(aspect*(IMH+v)), int(IMH+v)))
        img1.blit(img1_scale, (-aspect*v/2,-v/2))
        img1_scale.set_alpha((alpha_end-alpha))
        screen.blit(img1_scale,(img1_start,VSTART))
      
      if i >= mid-overlap:
        s = i-(mid-overlap)
        alpha = s * alpha_end / float(end-(mid-overlap))
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

 
