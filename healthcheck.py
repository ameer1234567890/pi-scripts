from __future__ import print_function
import time
import os

LOG_FILE = '/home/pi/pi-scripts/healthcheck.log'
INITIAL_WAIT_TIME = '60' # 60 seconds
INCREMENT_BY = 2 # multiply by 2

if os.path.isfile(LOG_FILE) == False:
    with open(LOG_FILE, 'w') as fh:
        fh.write(INITIAL_WAIT_TIME)

with open(LOG_FILE, 'r') as fh:
    last_wait_time = float(fh.read())

def ping_check():
    print('Checking for internet connectivity.')
    return os.system('ping -c 1 www.google.com')

def ping_success():
    print('Internet connectivity established.')
    now_wait_time = INITIAL_WAIT_TIME
    with open(LOG_FILE, 'w') as fh:
        fh.write(str(now_wait_time))

now_wait_time = last_wait_time * INCREMENT_BY

response = ping_check()
if response == 0:
    ping_success()
else:
    print('Error: {}'.format(response))
    print('Waiting for {} seconds'.format(now_wait_time))
    time.sleep(now_wait_time)
    response = ping_check()
    if response == 0:
        ping_success()
    else:
        print('Error: {}'.format(response))
        with open(LOG_FILE, 'w') as fh:
            fh.write(str(now_wait_time))
        print('Rebooting...')
        os.system('sudo reboot')
