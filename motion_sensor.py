from gpiozero import MotionSensor
from picamera import PiCamera
from time import sleep
import os

camera = PiCamera()
camera.resolution = (1280,720)
pir = MotionSensor(26, sample_rate=5,queue_len=3)
while True:
    pir.wait_for_motion()
    print('Motion detected')
    list = os.listdir('ca1/static/images/detected') # dir is your directory path
    number_files = len(list)
    sleep(3)
    camera.capture('ca1/static/images/detected/captured' + str(number_files) + '.jpg')
    pir.wait_for_no_motion()
    sleep(10)
