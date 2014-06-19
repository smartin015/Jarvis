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
  end = 100
  delta = DELTA
  fade_delay = 20
  end_movement = 40
  ghost = 0.50

  img1_start = float(-delta)
  img2_start = float(-1.5*delta)

  #screen.blit(img2,(img2_start,0))
  screen.blit(img1,(img1_start,0))
  pygame.display.flip()
  time.sleep(2.0)
  

  img2.set_alpha(255)
  last_v1 = 0
  last_v2 = 0
  for i in xrange(start, end):
    v1 = easeInOutQuad(i, start, delta, end)
    v2 = easeInOutQuad(i, start+40, delta/2, end)

    if i > end - end_movement:
      alpha = 255
    elif i > fade_delay:
      alpha = (i-fade_delay) * (255.0/float(end-fade_delay-end_movement))
    else:
      alpha = 0

    #img2.set_alpha(alpha)
    #screen.blit(img2,(img2_start+v2,0)) #image 2 in background

    #img1.set_alpha((255-alpha)*ghost)
    #screen.blit(img1,(img1_start+last_v1,0))
    img1.set_alpha((255-alpha))
    screen.blit(img1,(img1_start+v1,0))
    

    
    pygame.display.flip()

    last_v1 = v1
    last_v2 = v2
    clock.tick(30)


  time.sleep(1.0)


    


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
        

