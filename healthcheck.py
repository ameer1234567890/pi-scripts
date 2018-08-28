#!/usr/bin/sudo env/bin/python3
# *-* coding: utf-8 -*-
"""Check internet connectivity and reboot if necessary"""

from __future__ import print_function
import time
import os
import datetime

LOG_FILE = '/home/pi/pi-scripts/healthcheck.log'
EVENTS_FILE = '/home/pi/pi-scripts/healthevents.log'
RUN_INTERVAL = 60  # run every 60 seconds
INITIAL_WAIT_TIME = 30  # 30 seconds
INCREMENT_BY = 2  # multiply by 2
NUM_RETRIES = 3  # retry pinging 3 times before reboot


def run_check():
    print('Checking for internet connectivity.')
    global response
    response = os.system('ping -c 1 www.google.com >> /dev/null 2>&1')
    if response == 0:
        print('Internet connectivity established. Status: {}'.format(response))
        now_wait_time = INITIAL_WAIT_TIME
        write_log(str(now_wait_time))
        return 'success'
    else:
        print('No internet connectivity detected. Error: {}'.format(response))
        return 'fail'


def reboot_now():
    print('Error: {}'.format(response))
    write_log(str(now_wait_time))
    write_event('{} Rebooting due to unavailability of internet connection.\n'
                .format(datetime.datetime.now()))
    print('Rebooting...')
    os.system('sudo reboot')


def write_log(data):
    with open(LOG_FILE, 'w') as fh:
        fh.write(data)


def write_event(data):
    with open(EVENTS_FILE, 'a') as fh:
        fh.write(data)


if not os.path.isfile(LOG_FILE):
    write_log(str(INITIAL_WAIT_TIME))

with open(LOG_FILE, 'r') as fh:
    last_wait_time = float(fh.read())

tries = 0
now_wait_time = last_wait_time

while 1:
    now_wait_time = now_wait_time * INCREMENT_BY
    tries = tries + 1
    status = run_check()
    if (status == 'success'):
        tries = 0
        write_log(str(INITIAL_WAIT_TIME))
        print('Waiting for {} seconds for the next check'
              .format(RUN_INTERVAL))
        print('')
        time.sleep(RUN_INTERVAL)
    elif (status == 'fail'):
        write_event('{} Internet access unavailable.\n'
                    .format(datetime.datetime.now()))
        print('Waiting for {} seconds before we check again...'
              .format(now_wait_time))
        if (tries > NUM_RETRIES):
            print('{} times retried already. Giving up...'
                  .format(NUM_RETRIES))
            reboot_now()
        time.sleep(now_wait_time)
