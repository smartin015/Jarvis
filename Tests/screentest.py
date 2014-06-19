import time
from Outputs.ScreenController import ScreenController, PORT

#con = ScreenController("192.168.1.100", PORT)
con2 = ScreenController("Jarvis", PORT)

#con.set_img("forest.jpg")
time.sleep(0.1)
con2.set_img("Assets/Images/forest.jpg")

print "Set image"

time.sleep(2.0)

#con.zoom_to("grassland.jpg")
time.sleep(0.1)
con2.slide_to("Assets/Images/grassland.jpg")

print "Slid image"
time.sleep(2.0)
