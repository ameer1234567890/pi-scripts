from __future__ import print_function
import RPi.GPIO as GPIO
import requests
import time

PIN = 10

GPIO.setmode(GPIO.BCM)

with open('/home/pi/.maker_key', 'r') as key_file:
    maker_key = key_file.read()

def rc_time (PIN):
    count = 0
    GPIO.setup(PIN, GPIO.OUT)
    GPIO.output(PIN, 0)
    time.sleep(0.1)
    GPIO.setup(PIN, GPIO.IN)
    while (GPIO.input(PIN) == 0):
        count += 1
    return count

if __name__ == '__main__':
    light_level = rc_time(PIN)
    print('Light Level: {}'.format(str(light_level)))
    maker_url = 'https://maker.ifttt.com/trigger/light-sensor/with/key/' + maker_key + '?value1=' + str(light_level)
    content = requests.get(maker_url).text
    print(content)
