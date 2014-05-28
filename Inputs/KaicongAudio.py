from Kaicong import KaicongDevice

import audioop
import numpy as np

class KaicongAudio(KaicongDevice):
    HEADER_SIZE = 32 # Bytes
    PACKET_SIZE = 544 # Bytes
    URI = "http://%s:81/audiostream.cgi?user=%s&pwd=%s&streamid=2&filename="
    
    def __init__(self, domain, callback, user="admin", pwd="123456"):
        KaicongDevice.__init__(
            self, 
            callback,
            domain, 
            KaicongAudio.URI, 
            KaicongAudio.PACKET_SIZE, 
            user, 
            pwd
        )

    def convert(self, data):
        # Strip the header at the beginning of the data
        data = data[KaicongAudio.HEADER_SIZE:]
        
        # Decompress from ADPCM (differential) to PCM-16L (WAV) format
        result = ""
        state = None
        for i in xrange(0, len(data)-5, 2):  #TODO: No magic numbers
            adpcmfragment = data[i:i+2]
            (sample, state) = audioop.adpcm2lin(adpcmfragment, 2, state)
            result += sample
    
        return np.fromstring(result, dtype=np.int16) 
        
    def handle(self, data):
        self.callback(self.convert(data))
        
if __name__ == "__main__":
    #Demo of kaicong audio
    from ..Outputs.Speaker import Speaker
    spkr = Speaker()    
    audio = KaicongAudio("192.168.1.15", spkr.play)
    audio.run()
    
        