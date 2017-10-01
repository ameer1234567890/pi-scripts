from __future__ import print_function
import RPi.GPIO as GPIO
import os
import time
import datetime

PIN = 17
ROUTER_IP = '192.168.7.1'
LOG_FILE = '/home/pi/pi-scripts/routercheck.log'

print('Checking connectivity...')
response = os.system('ping -c 1 ' + ROUTER_IP + ' >> /dev/null 2>&1')

if response == 0:
    print('Router is OK!')
else:
    print('Either router is not working or Wifi is down. Rebooting Wifi...')
    wlan_if = os.popen('ifconfig | grep wl | cut -d : -f 1').read()
    os.system('sudo ifdown ' + wlan_if)
    os.system('sudo ifup ' + wlan_if)
    time.sleep(1)
    print('Checking connectivity...')
    response = os.system('ping -c 1 ' + ROUTER_IP + '>> /dev/null 2>&1')
    if response == 0:
        print('Router was OK! Wifi was down! Now OK!')
    else:
        print('Router is actually down! Rebooting router now...')
        with open(LOG_FILE, 'a') as fh:
          fh.write('{} Rebooting router!\n'.format(datetime.datetime.now()))
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN, GPIO.OUT)
        GPIO.output(PIN, 1)
        time.sleep(1)
        GPIO.output(PIN, 0)
        GPIO.cleanup()
