from __future__ import print_function
import RPi.GPIO as GPIO
import datetime
import time
import requests

KNOCK_PIN=23
BUZZER_PIN=22
GPIO.setmode(GPIO.BCM)
GPIO.setup(KNOCK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

while True:
    try:
        GPIO.wait_for_edge(KNOCK_PIN, GPIO.FALLING)
        GPIO.output(BUZZER_PIN, 1)
        time.sleep(0.1)
        GPIO.output(BUZZER_PIN, 0)
        print(datetime.datetime.now())
        content = requests.get('http://raspberrypi.local:26337/').text
        print(content)
    except:
        pass

GPIO.cleanup()
print('GPIO cleanup done!')
