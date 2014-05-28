import audioop

with open("audio_stripped_frames.pcm2", "rb") as f:
    data = f.read()
    
   
lin_data = ""
state = None
for i in xrange(0, len(data)-5, 2):
    adpcmfragment = data[i:i+2]
    (sample, state) = audioop.adpcm2lin(adpcmfragment, 2, state)
    lin_data += sample
    
out = open("audio_conversion_test.pcm2", "wb")
out.write(lin_data)
out.close()