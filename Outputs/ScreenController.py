import pygame
from pygame.locals import *
import os
import time

DELTA = 200

def tween(img1, img2):
  for i in xrange(255):
    img1.set_alpha(255-i)
    img2.set_alpha(i)
    screen.fill((0, 0, 0))
    screen.blit(img1,(0,0))
    screen.blit(img2,(0,0))
    pygame.display.flip()
    clock.tick(30)



def easeInOutQuad(currtime, start, delta, duration):
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

def blur_blit(img, last, curr, ghost=0.25):
  pass

def sweep(img1, img2):
  start = 0
  mid = 60
  overlap = 10
  end = 100
  delta = DELTA
  ghost = 0.50
  alpha_end = 150

  img1_start = float(-delta)
  img2_start = float(-2*delta)

  #screen.blit(img2,(img2_start,0))
  screen.blit(img1,(img1_start,0))
  pygame.display.flip()
  time.sleep(2.0)

  for i in xrange(start, end):
    v = easeInOutQuad(i, start, delta, end) 

    if i < mid+overlap:
      alpha = i * (alpha_end/float(mid+overlap))  
      img1.set_alpha((alpha_end-alpha))
      screen.blit(img1,(img1_start+v,0))
    
    if i > mid-overlap:
      alpha = (i-(mid-overlap)) * (alpha_end/float(end-(mid-overlap)))  
      img2.set_alpha(alpha)
      screen.blit(img2,(img2_start+v,0))
  
    pygame.display.flip()
    clock.tick(30)

def loadimg(path):
  img = pygame.image.load(path).convert()
  img = pygame.transform.scale(img, (SW+2*DELTA,SH))   
  return img

if __name__ == '__main__':
  os.environ["DISPLAY"] = ":0"

  SW,SH = 1920, 1080
  os.environ["SDL_FBDEV"] = "/dev/fb1"
  screen = pygame.display.set_mode((SW,SH), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
  clock = pygame.time.Clock()
  pygame.mouse.set_visible(False)

  #img1 = loadimg("Assets/screentest/dawn.jpg")
  #img2 = loadimg("Assets/screentest/day.jpg")
  #img3 = loadimg("Assets/screentest/dusk.jpg")
  img1 = loadimg("Assets/Images/grassland.jpg")
  img2 = loadimg("Assets/Images/forest.jpg")
  while True:
    sweep(img1, img2)
    sweep(img2, img1)
        

