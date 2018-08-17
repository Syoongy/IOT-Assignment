import MySQLdb
import RPi.GPIO as GPIO
import Adafruit_DHT
from time import sleep 
from gpiozero import MotionSensor
import picamera
import time
import threading
from threading import Thread

pir = MotionSensor(26, sample_rate=5,queue_len=1)
dht = 4
camera = picamera.PiCamera()

def collectDHTData():
  try:
    db = MySQLdb.connect("localhost", "assignmentuser", "dmitiot", "assignmentdatabase")
    curs = db.cursor()
    print("Successfully connected to database!")
  except:
    print("Error connecting to mySQL database")
  while True:
    humidity,temperature = Adafruit_DHT.read_retry(11,dht)
    temperature = format(temperature, '.1f')
    humidity = format(humidity, '.1f')
    sql = "INSERT into temphumid (temperature,humidity) VALUES (%s,%s)" % (str(temperature),str(humidity))
    print(sql)
    curs.execute(sql)
    db.commit()
    print("Wait 5 secs before getting next light values..")
    sleep(5)

def motionCamera():
  try:
    db = MySQLdb.connect("localhost", "assignmentuser", "dmitiot", "assignmentdatabase")
    curs = db.cursor()
    print("Successfully connected to database!")
  except:
    print("Error connecting to mySQL database")
  while True:
    pir.wait_for_motion()
    timestring = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
    print ("Taking photo " +timestring)
    camera.capture('/home/pi/labs/Assignment/static/PhotoGallery/photo_'+timestring+'.jpg')  
    imagepath = '\"' + timestring+'.jpg\"'
    sql = "INSERT into cameraphotos (image_address) VALUES (%s)" % (imagepath)
    print(sql)
    curs.execute(sql)
    db.commit()  
    sleep(5)

if __name__ == '__main__':
  Thread(target = collectDHTData).start()
  Thread(target = motionCamera).start()

