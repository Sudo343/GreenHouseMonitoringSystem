import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import pyfirmata
import sys
import urllib2

channel_id = 882623
key = '48PW4P20I7YCZREZ'

dht_pin = 16
sensor_name= Adafruit_DHT.DHT11

board = pyfirmata.Arduino('/dev/ttyACM0')
it = pyfirmata.util.Iterator(board)
it.start()
analog_0 = board.get_pin('a:0:i')
time.sleep(.1)
baseURL = 'https://api.thingspeak.com/update?api_key=48PW4P20I7YCZREZ' 

def fetchNuploadDat():
    
    while True:
        h, t = Adafruit_DHT.read_retry(sensor_name, dht_pin)
        s = (1-analog_0.read())*100
        try:
            f = urllib2.urlopen(baseURL +"&field1=%s" % (str(h)))
            f = urllib2.urlopen(baseURL +"&field2=%s" % (str(t)))
            f = urllib2.urlopen(baseURL +"&field3=%s" % (str(s)))
            f.close()
            sleep(1)
        except:
            print "connection failed"
        break
if __name__ == "__main__":
    while True:
        fetchNuploadDat()
        # free account has an api limit of 15sec
        time.sleep(1)
