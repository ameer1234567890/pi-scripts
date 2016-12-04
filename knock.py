#!/bin/python
import RPi.GPIO as GPIO
import os
import datetime
import time
import requests

gpio_pin_number=23
buzzer_pin=22
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buzzer_pin, GPIO.OUT)

while True:
    try:
        GPIO.wait_for_edge(gpio_pin_number, GPIO.FALLING)
        GPIO.output(buzzer_pin, True)
        time.sleep(0.1)
        GPIO.output(buzzer_pin, False)
        print(datetime.datetime.now())
        content = requests.get('http://raspberrypi.local:26337/').text
        print(content)
    except:
        pass

GPIO.cleanup()
print('GPIO cleanup done!')
