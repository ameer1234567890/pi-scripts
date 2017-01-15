# *-* coding: utf-8 -*-
import requests
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

humidity, temp = Adafruit_DHT.read_retry(SENSOR, PIN)

if humidity is not None and temp is not None:
    print('Temperature: {0:0.1f}°C Humidity: {1:0.1f}%'.format(temp, humidity))
    print('Uploading data to Weather Underground...')
    # build a weather data object
    weather_data = {
        'action': 'updateraw',
        'ID': Config.STATION_ID,
        'PASSWORD': Config.STATION_KEY,
        'dateutc': 'now',
        'tempf': str(c_to_f(temp)),
        'humidity': str(humidity),
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
