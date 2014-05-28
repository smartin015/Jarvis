import string
data = ""
with open("audio.pcm2", "rb") as f:
    data = f.read()
   
packet_width = 544
opener = data[packet_width: packet_width+32]
print "Opener:"
for i in opener:
    print hex(ord(i))
    
print "Data len:", len(data)
print string.find(data, opener)
idx = 0
last_idx = 0
while idx != -1:
    idx = string.find(data, opener, idx+1)
    print idx - last_idx
    last_idx = idx
        
        
        
#Attempt to strip out header information 
data_formatted = ""
i = 0
while i < len(data):
    packet = data[i:i+packet_width]
    packet_stripped = packet[33:]
    data_formatted += packet_stripped
    i += packet_width
        
out = open("audio_stripped_frames_try2.pcm2", "wb")
out.write(data_formatted)
out.close()
