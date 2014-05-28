import pygame
from pygame.locals import *

import math
import numpy

size = (1366, 720)

bits = 16
#the number of channels specified here is NOT 
#the channels talked about here http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.get_num_channels

pygame.mixer.pre_init(44100, -bits, 2)
pygame.init()
_display_surf = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)


duration = 1.0          # in seconds
#freqency for the left speaker
frequency_l = 440
#frequency for the right speaker
frequency_r = 550

#this sounds totally different coming out of a laptop versus coming out of headphones

sample_rate = 44100

n_samples = int(round(duration*sample_rate))

#setup our numpy array to handle 16 bit ints, which is what we set our mixer to expect with "bits" up above
buf = numpy.zeros((n_samples, 2), dtype = numpy.int16)
max_sample = 2**(bits - 1) - 1

for s in range(n_samples):
    t = float(s)/sample_rate    # time in seconds

    #grab the x-coordinate of the sine wave at a given time, while constraining the sample to what our mixer is set to with "bits"
    buf[s][0] = int(round(max_sample*math.sin(2*math.pi*frequency_l*t)))        # left
    buf[s][1] = int(round(max_sample*0.5*math.sin(2*math.pi*frequency_r*t)))    # right

sound = pygame.sndarray.make_sound(buf)
#play once, then loop forever
sound.play(loops = -1)


#This will keep the sound playing forever, the quit event handling allows the pygame window to close without crashing
_running = True
while _running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _running = False
            break

pygame.quit()