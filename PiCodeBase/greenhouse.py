import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import pyfirmata
import sys
import httplib
import urllib

channel_id = 882623
key = '48PW4P2OI7YCZREZ'

dht_pin = 16
sensor_name= Adafruit_DHT.DHT11

board = pyfirmata.Arduino('/dev/ttyACM0')
it = pyfirmata.util.Iterator(board)
it.start()
analog_0 = board.get_pin('a:0:i')   # soilmoisture sensor
analog_1 = board.get_pin('a:1:i')    # light dependent resistor
time.sleep(.1)
baseURL = 'https://api.thingspeak.com/update?api_key=48PW4P2OI7YCZREZ' 

def fetchNuploadDat():
    
    while True:
        h, t = Adafruit_DHT.read_retry(sensor_name, dht_pin)
        s = (1-analog_0.read())*100  # 
        l = (1-analog_1.read())*100  # needs calibration
        print(h)
        print(t)
        print(s)   # 
        print(l)
        params = urllib.urlencode({'field1':h,'field2':t,'field3':s,'field4':l,'key':key})  
        headers = {"Content-typZZe":"application/x-www-form-urlencoded","Accept":"text/plain"}
        conn=httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST","/update",params,headers)
            response = conn.getresponse()
            print(response.status,response.reason)
            data = response.read()
            conn.close()
            time.sleep(1)
        except:                        
            print "connection failed"  
        break
if __name__ == "__main__":
    while True:
        fetchNuploadDat()
        # free account has an api limit of 15sec
        time.sleep(600)
