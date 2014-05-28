import pyaudio 
import numpy as np 
import wave 

class Speaker:
    def __init__(self):
        chunk = 1016 
        FORMAT = pyaudio.paInt16 
        CHANNELS = 1 
        RATE = 8000 
        self.p = pyaudio.PyAudio() 
        self.stream = self.p.open(format = FORMAT, 
                        channels = CHANNELS, 
                        rate = RATE, 
                        input = True, 
                        output = True, 
                        frames_per_buffer = chunk) 
        
    def play(self, numpy_buf):
        signal = wave.struct.pack("%dh"%(len(numpy_buf)), *list(numpy_buf))
        self.stream.write(signal) 
        
    def __del__(self):
        self.stream.stop_stream() 
        self.stream.close() 
        self.p.terminate() 