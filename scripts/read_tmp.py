import sys
import Adafruit_DHT


def readTemp():
    pin = 4
    humidity, temperature = Adafruit_DHT.read_retry(11, pin)
    returnData = []
    returnData.append('{:.1f} %'.format(humidity))
    returnData.append('{:.1f} C'.format(temperature))
    return returnData
