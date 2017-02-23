# *-* coding: utf-8 -*-
from __future__ import print_function
import vcgencmd
import requests
import os
import time

temp_limit = 50
notify_interval = 30
log_file_path = '/home/pi/pi-scripts/pitemp.log'

with open('/home/pi/.maker_key', 'r') as key_file:
    maker_key = key_file.read()

cpu_temp = vcgencmd.measure_temp()

if os.path.isfile(log_file_path) == False:
    with open(log_file_path, 'w') as log_file:
        log_file.write('%s' % time.time())

with open(log_file_path, 'r') as log_file:
    time_last_notif = float(log_file.read())

maker_url = 'https://maker.ifttt.com/trigger/pitemp/with/key/' + maker_key + '?value1=' + str(cpu_temp)
content = requests.get(maker_url).text
print(content)

if cpu_temp > temp_limit:
    time_now = time.time()
    if time_now > time_last_notif + notify_interval:
        print('High and notify - {}°C'.format(str(cpu_temp)))
        maker_url = 'https://maker.ifttt.com/trigger/pitemp-over/with/key/' + maker_key + '?value1=' + str(cpu_temp)
        content = requests.get(maker_url).text
        print(content)
        with open(log_file_path, 'w') as log_file:
            log_file.write(time.time())
    else:
        print('High and not notify - {}°C'.format(str(cpu_temp)))
else:
    print('Not high - {}°C'.format(str(cpu_temp)))
