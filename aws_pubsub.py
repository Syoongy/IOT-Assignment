# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time,sys,picamera
from gpiozero import LED, Button
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from signal import pause
from rpi_lcd import LCD
import Adafruit_DHT
import json

ledRed = LED(18)
ledGreen = LED(17)
camera = picamera.PiCamera()
button = Button(13, pull_up=False)
lcd = LCD()
DHT11pin = 4
fridgeName = "fridge1"


AWS_ACCESS = "AKIAICF67YQCBBZZUYAQ"
AWS_SECRET = "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"

conn = S3Connection(AWS_ACCESS,AWS_SECRET)
bucket = conn.get_bucket('iot-fridge')

# Custom MQTT message callback
def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")
	
host = "alve3kumwqjo.iot.us-east-1.amazonaws.com"
rootCAPath = "rootca.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"

my_rpi = AWSIoTMQTTClient("basicPubSub")
my_rpi.configureEndpoint(host, 8883)
my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
my_rpi.configureMQTTOperationTimeout(5)  # 5 sec

def displayDHT11ValueOnLCD():
    humidity, temperature = Adafruit_DHT.read_retry(11, DHT11pin)
    lcd.text('Temp: {:.1f} C'.format(temperature), 1)
    print('Temp: {:.1f} C'.format(temperature))
    lcd.text('Humidity: {:.1f}'.format(humidity), 2)
    print('Humidity: {:.1f}'.format(humidity))


def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()

def takePictureAndUploadToS3():
    timestring = time.strftime("%Y-%m-%dT%H_%M_%S", time.gmtime())
    filename = fridgeName+'_item_'+timestring+'.jpg'
    camera.capture('/home/pi/'+filename)   
    k = Key(bucket)
    k.key = filename
    k.set_contents_from_filename('/home/pi/'+filename, cb=percent_cb, num_cb=10)
    publishImageName(filename)


# Publish image to AWS IOT broker
def publishImageName(name):
    data = json.dumps({"filaname":str(name)})
    my_rpi.publish(fridgeName+"/itemImage",data, 1)

# Publish temperature to AWS IOT broker
def publishDHT11():
    humidity,temperature = Adafruit_DHT.read_retry(11,DHT11pin)
    temperature = format(temperature, '.1f')
    humidity = format(humidity, '.1f')
    my_rpi.publish(fridgeName+"/temperature", str(temperature), 1)
    my_rpi.publish(fridgeName+"/humidity", str(humidity), 1)




def ledRedON():
    ledRed.on()
    print("red LED is on")
    time.sleep(2)
    ledRed.off()


def ledRedOFF():
    ledRed.off()
    print("red LED is off")

def ledGreenON():
    ledGreen.on()
    print("green LED is on")
    time.sleep(2)
    ledGreen.off()


def ledGreenOFF():
    ledGreen.off()
    print("green LED is off")

button.when_pressed = takePictureAndUploadToS3

#button.when_pressed = ledRedON
#button.when_released = ledGreenON


# Connect and subscribe to AWS IoT
my_rpi.connect()
my_rpi.subscribe("alert", 1, customCallback)
# if there are things going to expire in fridge today, it will receive an alert

while True:
	displayDHT11ValueOnLCD()
	publishDHT11()
	time.sleep(5)







