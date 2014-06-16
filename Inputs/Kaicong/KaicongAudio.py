from KaicongInput import KaicongInput
import audioop

class KaicongAudio(KaicongInput):
    HEADER_SIZE = 32 # Bytes
    PACKET_SIZE = 544 # Bytes
    URI = "http://%s:81/audiostream.cgi?user=%s&pwd=%s&streamid=2&filename="
    
    def __init__(self, domain, callback=None, user="admin", pwd="123456"):
        KaicongInput.__init__(
            self, 
            callback,
            domain, 
            KaicongAudio.URI, 
            KaicongAudio.PACKET_SIZE, 
            user, 
            pwd
        )

    def handle(self, data):
        # Strip the header at the beginning of the data
        data = data[KaicongAudio.HEADER_SIZE:]
        
        # Decompress from ADPCM (differential) to PCM-16L (WAV) format
        result = ""
        state = None
        for i in xrange(0, len(data)-5, 2):  #TODO: No magic numbers
            adpcmfragment = data[i:i+2]
            (sample, state) = audioop.adpcm2lin(adpcmfragment, 2, state)
            result += sample
    
        return result
        
        
if __name__ == "__main__":
    #Demo of kaicong audio
    import numpy as np
    from Outputs.Speaker import Speaker
    spkr = Speaker()    
    def play(data):
        spkr.play(np.fromstring(data, dtype=np.int16))
    audio = KaicongAudio("192.168.1.19", play, user="jarvis_admin", pwd="oakdale43")
    audio.run()
    
        
