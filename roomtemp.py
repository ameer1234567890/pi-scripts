# *-* coding: utf-8 -*-
from __future__ import print_function
import re
import requests
import Adafruit_DHT
import math
exec(open('/home/pi/.wu_config.py').read())

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 18
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

with open('/home/pi/.maker_key', 'r') as key_file:
    maker_key = key_file.read()

with open('/sys/bus/w1/devices/28-031663113dff/w1_slave', 'r') as temp_file:
    for line in temp_file:
        line = re.findall(r't=.*', line)
        if line:
            line = line[0].split('=')[1]
            ds_temp0 = int(line)

ds_temp1 = int(round((ds_temp0 / 1000), 0))
ds_temp2 = int(round((ds_temp0 / 100), 0))
ds_tempM = ds_temp2 % ds_temp1
ds_temp = str(ds_temp1) + '.' + str(ds_tempM)
print('DS Temperature: %s°C' % str(ds_temp))

dht_humidity, dht_temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

if dht_humidity is not None and dht_temp is not None:
    print('DHT Temperature: {0:0.1f}°C DHT Humidity: {1:0.1f}%'.format(dht_temp, dht_humidity))
    dewpoint = dew_point(int(float(ds_temp)), dht_humidity)
    print('Dew Point: {}°C'.format(str(round(dewpoint, 2))))

    # Post to Weather Underground PWS (Personal Weather Station)
    print('Uploading data to Weather Underground...')
    weather_data = {
        'action': 'updateraw',
        'ID': Config.STATION_ID,
        'PASSWORD': Config.STATION_KEY,
        'dateutc': 'now',
        'tempf': str(c_to_f(int(float(ds_temp)))),
        'humidity': str(dht_humidity),
        'dewptf': str(c_to_f(dewpoint)),
    }
    s = requests.Session()
    s.params = (weather_data)
    r = s.get(WU_URL)
    print("Status: {}".format(r.text))

    # Post to Google Spreadsheet via IFTTT
    print('Triggerring IFTTT event...')
    maker_url = 'https://maker.ifttt.com/trigger/roomtemp/with/key/' + maker_key + '?value1=' + ds_temp + '&value2=' + str(dht_humidity) + '&value3=' + str(round(dewpoint, 2))
    r = requests.get(maker_url)
    print(r.text)
else:
    dht_temp = 0
    dht_humidity = 0
    print('Failed to get DHT reading. Try again!')
