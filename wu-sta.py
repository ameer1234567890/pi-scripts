# *-* coding: utf-8 -*-
import requests
import math
import Adafruit_DHT
execfile('/home/pi/.wu_config.py')
from urllib import urlencode
import urllib2

SENSOR = Adafruit_DHT.DHT11
PIN = 18
WU_URL = "http://weatherstation.wunderground.com/weatherstation/updateweatherstation.php"

def c_to_f(input_temp):
    # convert input_temp from Celsius to Fahrenheit
    return (input_temp * 1.8) + 32

def dew_point(celsius, humidity):
    a = 17.271
    b = 237.7
    temp = (a * celsius) / (b + celsius) + math.log(humidity*0.01)
    dew = (b * temp) / (a - temp)
    return dew

humidity, temp = Adafruit_DHT.read_retry(SENSOR, PIN)

if humidity is not None and temp is not None:
    print('Temperature: {0:0.1f}°C Humidity: {1:0.1f}%'.format(temp, humidity))
    dewpoint = dew_point(temp, humidity)
    print('Dew Point: %s°C' % str(round(dewpoint, 2)))
    print('Uploading data to Weather Underground...')
    # build a weather data object
    weather_data = {
        'action': 'updateraw',
        'ID': Config.STATION_ID,
        'PASSWORD': Config.STATION_KEY,
        'dateutc': 'now',
        'tempf': str(c_to_f(temp)),
        'humidity': str(humidity),
        'dewptf': str(c_to_f(dewpoint)),
    }
    upload_url = WU_URL + '?' + urlencode(weather_data)
    response = urllib2.urlopen(upload_url)
    html = response.read()
    print('Server response: ' + html)
    response.close()
else:
    temp = 0
    humidity = 0
    print('Failed to get reading. Try again!')
