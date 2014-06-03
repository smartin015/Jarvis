import pyaudio
import struct
from Outputs.Speaker import Speaker
import numpy as np

FORMAT = pyaudio.paInt16 
CHANNELS = 1
RATE = 8000  
INPUT_FRAMES = 2014

pa = pyaudio.PyAudio()              
                                     
stream = pa.open(format = FORMAT,     
         channels = CHANNELS,          
         rate = RATE,                   
         input = True,                   
         frames_per_buffer = INPUT_FRAMES)

spkr = Speaker()

for i in range(1000):
    try:                                                   
        block = stream.read(INPUT_FRAMES)   
        spkr.play(np.fromstring(block, np.int16))
    except IOError, e:                                   
        print( "(%d) Error recording: %s"%(errorcount,e) )

