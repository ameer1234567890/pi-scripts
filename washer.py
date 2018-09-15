#!/usr/bin/sudo env/bin/python3
# *-* coding: utf-8 -*-
"""Turn on and off the washer in 30 minute intervals"""

from __future__ import print_function
import os
import time
import argparse

INTERVAL = 1800  # 30 minutes
DELAY_BETWEEN = 4
DEFAULT_ROUNDS = 4
TYPE = "0x2728"
HOST = "192.168.7.146"
MAC = "8db8c10d43b4"

parser = argparse.ArgumentParser(description='Example \
    with non-optional arguments')
parser.add_argument('--rounds', action="store", type=int)
results = parser.parse_args()

rounds = results.rounds
if rounds is None:
    rounds = DEFAULT_ROUNDS

for _i in range(0, rounds):
    os.system('env/bin/python3 python-broadlink/cli/broadlink_cli --type ' + TYPE +
              ' --host ' + HOST + ' --mac ' + MAC + ' --turnon')
    time.sleep(INTERVAL)
    os.system('env/bin/python3 python-broadlink/cli/broadlink_cli --type ' + TYPE +
              ' --host ' + HOST + ' --mac ' + MAC + ' --turnoff')
    time.sleep(DELAY_BETWEEN)
