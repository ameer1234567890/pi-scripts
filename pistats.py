# *-* coding: utf-8 -*-
from __future__ import print_function
import requests
import psutil
exec(open('/home/pi/.thingspeak_config.py').read())

cpu_pc = psutil.cpu_percent()
mem_avail_mb = round((psutil.virtual_memory().available/1000000), 2)

print('CPU Usage: {}%'.format(cpu_pc))
print('Available Memory: {}MB'.format(mem_avail_mb))

print('Posting to ThingSpeak...')
channel_url = 'https://api.thingspeak.com/update?api_key=' + Config.CHANNEL_KEY + '&field1=' + str(cpu_pc) + '&field2=' + str(mem_avail_mb)
print(channel_url)
print(r.text)
