from __future__ import print_function
import RPi.GPIO as GPIO
import os
import time
import datetime

PIN = 17
ROUTER_IP = '192.168.7.1'
LOG_FILE = '/home/pi/pi-scripts/routercheck.log'
INTERVAL = 60 # in seconds

def ping_test():
    print('{} Checking connectivity...'.format(datetime.datetime.now()))
    return os.system('ping -c 1 ' + ROUTER_IP + ' >> /dev/null 2>&1')

def restart_wlan_if():
    time.sleep(15)
    #wlan_if = os.popen('ifconfig | grep wl | cut -d : -f 1').read()
    #os.system('sudo ifdown ' + wlan_if)
    #os.system('sudo ifup ' + wlan_if)

while True:
    i = 1
    while i in range(1,3):
        response = ping_test()
        if response == 0:
            print('Router is OK!')
            break
        else:
            time.sleep(3)
            i = i + 1
    else:
        print('{} Either router is not working or Wifi interface is down. Restarting Wifi interface...'.format(datetime.datetime.now()))
        restart_wlan_if()
        time.sleep(5)
        response = ping_test()
        if response == 0:
            print('{} Router was OK! Wifi interface was down! Now OK!'.format(datetime.datetime.now()))
        else:
            print('{} Router is actually down! Rebooting router now...'.format(datetime.datetime.now()))
            with open(LOG_FILE, 'a') as fh:
                fh.write('{} Rebooting router!\n'.format(datetime.datetime.now()))
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(PIN, GPIO.OUT)
            GPIO.output(PIN, 1)
            time.sleep(1)
            GPIO.output(PIN, 0)
            GPIO.cleanup()
            time.sleep(30)
    print('======= DONE =======')
    time.sleep(INTERVAL)
