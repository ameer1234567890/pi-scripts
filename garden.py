# *-* coding: utf-8 -*-
from __future__ import print_function
import requests
import math
import time
import RPi.GPIO as GPIO
import Adafruit_DHT
exec(open('/home/pi/.thingspeak_config.py').read())

SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 24
LDR_PIN = 18

GPIO.setmode(GPIO.BCM)

def c_to_f(input_temp):
    # convert input_temp from Celsius to Fahrenheit
    return (input_temp * 9 / 5) + 32

def f_to_c(input_temp):
    # convert input_temp from Fahrenheit to Celsius
    return (input_temp - 32) * 5 / 9

def dew_point(temperature, humidity):
    a = 17.271
    b = 237.7
    temp = (a * temperature) / (b + temperature) + math.log(humidity*0.01)
    dew = (b * temp) / (a - temp)
    return dew

def heat_index(temperature, humidity):
    # http://en.wikipedia.org/wiki/Heat_index#Formula
    c1 = -42.379
    c2 = 2.04901523
    c3 = 10.14333127
    c4 = -0.22475541
    c5 = -6.83783e-3
    c6 = -5.481717e-2
    c7 = 1.22874e-3
    c8 = 8.5282e-4
    c9 = -1.99e-6
    temp = c_to_f(temperature)
    rel_humidity = humidity
    p1 = c1 + c2 * temp + c3*rel_humidity
    p2 = c4*temp*rel_humidity + c5*temp**2 + c6*rel_humidity**2
    p3 = c7*temp**2*rel_humidity + c8*temp*rel_humidity**2 + c9*temp**2*rel_humidity**2
    heat_index = p1 + p2 + p3
    return f_to_c(heat_index)

def rc_time(pin):
    count = 0
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)
    time.sleep(0.1)
    GPIO.setup(pin, GPIO.IN)
    while (GPIO.input(pin) == 0):
        count += 1
    return count

light_level = rc_time(LDR_PIN)
print('Light Level: {}'.format(str(light_level)))

humidity, temperature = Adafruit_DHT.read_retry(SENSOR, DHT_PIN)
if humidity is not None and temperature is not None:
    print('Temp={0:0.2f}°C  Humidity={1:0.2f}%'.format(temperature, humidity))
    dewpoint = dew_point(temperature, humidity)
    print('Dew Point: {}°C'.format(str(round(dewpoint, 2))))
    heatindex = heat_index(temperature, humidity)
    print('Heat Index: {}°C'.format(str(round(heatindex, 2))))
	
    # Post to ThingSpeak
    print('Posting to ThingSpeak...')
    channel_url = 'https://api.thingspeak.com/update?api_key=' + Config.CHANNEL_KEY + '&field1=' + str(round(temperature, 2)) + '&field2=' + str(round(humidity, 2)) + '&field3=' + str(round(dewpoint, 2)) + '&field4=' + str(round(heatindex, 2)) + '&field5=' + str(light_level)
    r = requests.get(channel_url)
    print(r.text)
else:
    print('Failed to get reading. Try again!')
