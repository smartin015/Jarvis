from cv2 import *
from cv2 import cv
import urllib
import numpy as np
k=0
capture=cv.CaptureFromFile("http://192.168.1.252:81/livestream.cgi?user=admin&pwd=123456&streamid=3&audio=0&filename=")
namedWindow("Display",1)

while True:
    frame=cv.QueryFrame(capture)
    if frame is None:
        print 'Cam not found'
        break
    else:
        cv.ShowImage("Display", frame)
    if k==0x1b:
        print 'Esc. Exiting'
        break
