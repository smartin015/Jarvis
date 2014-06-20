import time
from Outputs.AudioController import AudioController, PORT
import socket

con = AudioController("192.168.1.100", PORT)


con.play("confirm2")
print "Played sound"
