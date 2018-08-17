from importlib import import_module
import os
import MySQLdb
import RPi.GPIO as GPIO
from flask import Flask, request, Response, render_template, jsonify
from gpiozero import LED, Buzzer, MotionSensor
from signal import pause
import picamera
import sys
import Adafruit_DHT
from time import sleep
import json 

app = Flask(__name__)
GPIO.setmode(GPIO.BCM) 
CHANNEL=16  
GPIO.setup(CHANNEL,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
dht = 4
led = LED(18)
bz = Buzzer(5)
pir = MotionSensor(26, sample_rate=5,queue_len=1)

def buzzerOn():
  bz.on()
  return "On"

def buzzerOff():
  bz.off()
  return "Off"

def ledOn():
  led.on()
  return "On"

def ledOff():
  led.off()
  return "Off"

def ledBlink():
  led.blink()
  return "Blink"

def ledStatus():
  if led.is_lit:
     return 'On'
  else:
    return 'Off'

@app.route("/")
def index():
   response = ledStatus()

   templateData = {
      'title' : 'Status of LED: ',
      'led_status' : response,
      'buzzer_status' : 'Off'
   }

   return render_template('index.html', **templateData)
     
@app.route("/writeLED/<status>")
def writeLED(status):
   if status == 'On':
     response = ledOn()
   elif status == 'Blink':
     response = ledBlink()
   else:
     response = ledOff()

   templateData = {
      'title' : 'Status of LED',
      'led_status' : response,
      'buzzer_status' : 'Off'
   }

   return render_template('index.html', **templateData)

@app.route("/writeBuzzer/<status>")
def writeBuzzer(status):
   led_status = ledStatus()
   if status == 'On':
     response = buzzerOn()
   else:
     response = buzzerOff()

   templateData = {
      'title' : 'Status of LED',
      'led_status' : led_status,
      'buzzer_status' : response
   }

   return render_template('index.html', **templateData)

@app.route("/realtime")
def getrealtimedata():
  db = MySQLdb.connect("localhost", "assignmentuser", "dmitiot", "assignmentdatabase")
  print("Database successfully connected")
  cur = db.cursor()
  query = "SELECT datetime_value, temperature, humidity FROM temphumid ORDER BY datetime_value DESC LIMIT 1"
  cur.execute(query)
  row = cur.fetchone ()
  status=GPIO.input(CHANNEL) 
  if status == True: 
    message = 'Monitoring dangerous gas...'      
  else:   
    message = 'Dangerous gas is detected!'
  templateData = {
    'temperature' : row[1],
    'humidity' : row[2],
     'gas' : message
  }
  return render_template('realtimeData.html',  **templateData)

def cleanData(original):
  newString = original.replace("(", "")
  newString = newString.replace(")", "")
  newString = newString.replace(",", "")
  newString = newString.replace("\"", "")
  newString = newString.replace("\'", "")
  return newString


@app.route("/temphistory")
def temphistory():  
  db = MySQLdb.connect("localhost", "assignmentuser", "dmitiot", "assignmentdatabase")
  print("Database successfully connected")
  cur = db.cursor()
  query = "SELECT datetime_value, temperature FROM temphumid ORDER BY datetime_value DESC LIMIT 10"
  cur.execute(query)
  data = []
  number = 1
  for (datetime_value, temperature) in cur:
    d = []
    d.append("{:%H:%M:%S}".format(datetime_value))
    d.append(temperature)
    d.append(number)
    data.append(d)    
  print(data)
  data_reversed = data[::-1]
  return render_template('temperatureHistory.html',  data=data_reversed)

@app.route("/humhistory")
def humhistory():  
  db = MySQLdb.connect("localhost", "assignmentuser", "dmitiot", "assignmentdatabase")
  print("Database successfully connected")
  cur = db.cursor()
  query = "SELECT datetime_value, humidity FROM temphumid ORDER BY datetime_value DESC LIMIT 10"
  cur.execute(query)
  data = []
  for (datetime_value, humidity) in cur:
    d = []
    d.append("{:%H:%M:%S}".format(datetime_value))
    d.append(humidity)
    data.append(d)    
  print(data)
  data_reversed = data[::-1]
  return render_template('humidityHistory.html',  data=data_reversed)

@app.route("/photo")
def photogallery():
  db = MySQLdb.connect("localhost", "assignmentuser", "dmitiot", "assignmentdatabase")
  print("Database successfully connected")
  cur = db.cursor()
  query = "SELECT image_address FROM cameraphotos ORDER BY datetime_value DESC LIMIT 5"
  cur.execute(query)
  data = cur.fetchall()
  print(data[0])
  templateData = {
    'image1' : cleanData(str(data[0])),
    'image2' : cleanData(str(data[1])),
    'image3' : cleanData(str(data[2])),
    'image4' : cleanData(str(data[3])),
    'image5' : cleanData(str(data[4]))
  }
  return render_template('photoGallery.html',  **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000, debug=True)