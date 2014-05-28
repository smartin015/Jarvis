import pygame
from pygame.locals import *

import math
import numpy

size = (320, 240)

bits = 16
#the number of channels specified here is NOT 
#the channels talked about here http://www.pygame.org/docs/ref/mixer.html#pygame.mixer.get_num_channels

pygame.mixer.pre_init(frequency=8000, size=-bits, channels=1)
pygame.init()
_display_surf = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)


duration = 1.0          # in seconds
#freqency for the left speaker
frequency_l = 300
#frequency for the right speaker
frequency_r = 550

#this sounds totally different coming out of a laptop versus coming out of headphones

sample_rate = 8000

n_samples = int(round(duration*sample_rate))

#setup our numpy array to handle 16 bit ints, which is what we set our mixer to expect with "bits" up above
with open("audio_conversion_test.pcm2", "rb") as f:
    data = f.read()
    
print len(data)
buf = numpy.fromstring(data)
print numpy.size(buf)
sound = pygame.sndarray.make_sound(buf)
#play once, then loop forever
sound.play()


#This will keep the sound playing forever, the quit event handling allows the pygame window to close without crashing
_running = True
while _running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _running = False
            break

pygame.quit()