#!/usr/bin/sudo env/bin/python3
# *-* coding: utf-8 -*-
"""Log Raspberry Pi's temperature to a spreadsheet via IFTTT"""

from __future__ import print_function
import vcgencmd
import requests
import os
import time

TEMP_LIMIT = 50
NOTIFY_INTERVAL = 30
INTERVAL = 60  # in seconds
LOG_FILE = '/home/pi/pi-scripts/pitemp.log'
MAKER_BASE_URL = 'https://maker.ifttt.com/trigger/pitemp-over/with/key/'


with open('/home/pi/.maker_key', 'r') as key_file:
    maker_key = key_file.read()


while True:

    cpu_temp = vcgencmd.measure_temp()

    if not os.path.isfile(LOG_FILE):
        with open(LOG_FILE, 'w') as fh:
            fh.write('%s' % time.time())

    with open(LOG_FILE, 'r') as fh:
        time_last_notif = float(fh.read())

    maker_url = 'https://maker.ifttt.com/trigger/pitemp/with/key/' \
                + maker_key + '?value1=' + str(cpu_temp)
    content = requests.get(maker_url).text
    print(content)

    if cpu_temp > TEMP_LIMIT:
        time_now = time.time()
        if time_now > time_last_notif + NOTIFY_INTERVAL:
            print('High and notify - {}°C'.format(str(cpu_temp)))
            maker_url = MAKER_BASE_URL + maker_key + '?value1=' \
                + str(cpu_temp)
            content = requests.get(maker_url).text
            print(content)
            with open(LOG_FILE, 'w') as fh:
                fh.write('%s' % time.time())
        else:
            print('High and not notify - {}°C'.format(str(cpu_temp)))
    else:
        print('Not high - {}°C'.format(str(cpu_temp)))

    print('======= DONE =======')
    time.sleep(INTERVAL)
