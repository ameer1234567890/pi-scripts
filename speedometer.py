import wiringpi
import time
import re
import math
import os

PIN_BASE = 65
I2C_ADDR = 0x20
MCP_PINS = [65, 66, 67, 68, 69, 70, 71, 72, 73, 74]
LOG_FILE = '/home/pi/pi-scripts/speedtest.log'
WAIT_FOR_FILE = 90

def get_speed():
    global speed
    with open(LOG_FILE, 'r') as log_file:
        for line in log_file:
            line = re.findall(r'Download.*', line)
            if line:
                line = line[0].split(': ')[1].split(' Mbit/s')[0]
                speed = int(math.ceil(float(line)))
                if speed > 10: speed = 10

if os.stat(LOG_FILE).st_size == 0:
    print('Empty log file. Retrying after ' + str(WAIT_FOR_FILE) + ' seconds...')
    time.sleep(WAIT_FOR_FILE)
    if os.stat(LOG_FILE).st_size == 0:
        print('Empty log file. There seems to be some error!')
        print('Exiting...')
        exit()
    else:
        get_speed()
else:
    get_speed()

print('Speed: ' + str(speed))

wiringpi.wiringPiSetup()
wiringpi.mcp23017Setup(PIN_BASE,I2C_ADDR)

for PIN in MCP_PINS:
    wiringpi.pinMode(PIN, 1)

i = 1
for PIN in MCP_PINS:
    if speed >= i:
        wiringpi.digitalWrite(PIN, 1)
    else:
        wiringpi.digitalWrite(PIN, 0)
    i += 1
