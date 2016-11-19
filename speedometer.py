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
SPEED_LIMIT = 10
NUM_LEDS = len(MCP_PINS)

def get_speed():
    global speed
    global raw_speed
    with open(LOG_FILE, 'r') as log_file:
        for line in log_file:
            line = re.findall(r'Download.*', line)
            if line:
                line = line[0].split(': ')[1].split(' Mbit/s')[0]
                raw_speed = line
                speed = int(math.ceil(float(line)))
                if speed > SPEED_LIMIT: speed = SPEED_LIMIT

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

print('Speed: ' + str(raw_speed) + ' Mbits/s')

speed_percent = (speed * 100) / SPEED_LIMIT
leds_lit = (NUM_LEDS * speed_percent) / 100
print('LEDs lit: ' + str(leds_lit) + '/' + str(NUM_LEDS))

wiringpi.wiringPiSetup()
wiringpi.mcp23017Setup(PIN_BASE,I2C_ADDR)

for PIN in MCP_PINS:
    wiringpi.pinMode(PIN, 1)

i = 1
for PIN in MCP_PINS:
    if leds_lit >= i:
        wiringpi.digitalWrite(PIN, 1)
    else:
        wiringpi.digitalWrite(PIN, 0)
    i += 1
