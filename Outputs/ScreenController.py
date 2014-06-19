import pygame
from pygame.locals import *
import os
import time
import socket
import threading

SW,SH = 1920, 1080
DELTA = 400
SCALE_DELTA = 10
VSTART = 0
IMW, IMH = SW+2*DELTA, SH+SCALE_DELTA


class ScreenServer(threading.Thread):
  def __init__(self, host, port):
    threading.Thread.__init__(self)
    self.s = socket.socket()         # Create a socket object
    self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.s.bind((host, port))        # Bind to the port
    self.s.listen(5)                 # Now wait for client connection.

  def run(self):
    os.environ["DISPLAY"] = ":0"
    os.environ["SDL_FBDEV"] = "/dev/fb1"
    self.screen = pygame.display.set_mode(
      (SW,SH), 
      pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
    )
    self.clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)

    img1 = loadimg("Assets/Images/grassland.jpg")
    img2 = loadimg("Assets/Images/forest.jpg")
    while True:
      #c, addr = self.s.accept()     # Establish connection with client.
      #print 'Got connection from', addr
      #c.send('Thank you for connecting')
      #c.close()                # Close the connection
      self.zoom(img1, img2, DELTA)
      time.sleep(2.0)
      self.sweep(img2,img1, DELTA)
      time.sleep(2.0)

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

  def sweep(self, img1, img2, delta):
    start = 0
    mid = 60
    overlap = 10
    end = 100
    alpha_end = 150
    img1_start = float(-delta)
    img2_start = float(-2*delta)

    for i in xrange(start, end):
      v = ScreenServer.easeInOutQuad(i, start, delta, end) 

      if i < mid+overlap:
        alpha = i * (alpha_end/float(mid+overlap))  
        img1.set_alpha((alpha_end-alpha))
        self.screen.blit(img1,(img1_start+v,VSTART))
    
      if i > mid-overlap:
        alpha = (i-(mid-overlap)) * (alpha_end/float(end-(mid-overlap)))  
        img2.set_alpha(alpha)
        self.screen.blit(img2,(img2_start+v,VSTART))
  
    pygame.display.flip()
    self.clock.tick(30)

  def zoom(self, img1, img2, delta):
    start = 0
    mid = 90
    overlap = 20
    end = 100
    alpha_end = 150
    img1_start = float(-delta)
    img2_start = float(-delta)
    delta /= 4
    aspect = float(IMW)/float(IMH)

    img1 = img1.copy()

    for i in xrange(start, end):
      v = ScreenServer.easeInOutQuad(i, start, delta, end) 

      if i < mid+overlap:
        alpha = i * (alpha_end/float(mid+overlap))  
        img1_scale = pygame.transform.smoothscale(img1, (int(aspect*(IMH+v)), int(IMH+v)))
        img1.blit(img1_scale, (-aspect*v/2,-v/2))
        img1_scale.set_alpha((alpha_end-alpha))
        self.screen.blit(img1_scale,(img1_start,VSTART))
      
      if i > mid-overlap:
        alpha = (i-(mid-overlap)) * (alpha_end/float(end-(mid-overlap)))
        img2.set_alpha(alpha)
        self.screen.blit(img2,(img2_start,VSTART+float(i-end)/2))
    
      pygame.display.flip()
      self.clock.tick(60)

class ScreenController(threading.Thread):
  def __init__(self, host, port):
    s = socket.socket()         # Create a socket object
    print "Connecting to", host
    s.connect((host, port))
    print s.recv(1024)
    s.close                     # Close the socket when done



def loadimg(path):
  img = pygame.image.load(path).convert()
  img = pygame.transform.scale(img, (IMW,IMH))   
  return img

if __name__ == '__main__':
  host = socket.gethostname() # Get local machine name
  port = 9808
  srv = ScreenServer(host, port)
  srv.daemon = True
  srv.start()
  con = ScreenController(host, port)
  time.sleep(10.0)
"""
  
        
"""
