from picamera import PiCamera
from time import sleep
import os

def takeImg():
    for file in os.listdir("ca1/static/images"):
        if file.endswith(".jpg"):
            os.remove(os.path.join("ca1/static/images", file))
    camera = PiCamera()
    camera.resolution = (1280,720)
    sleep(3)
    camera.capture('ca1/static/images/test.jpg')
