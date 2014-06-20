import time
from Outputs.AudioController import AudioController, PORT
import socket

con = AudioController(socket.gethostname(), PORT)


con.play("confirm")
print "Played sound"
