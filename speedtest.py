from __future__ import print_function
import os
import requests
import math
import time
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.MCP230xx as MCP230xx

PIN_BASE = 0
I2C_ADDR = 0x20
MCP_PINS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
MCP_PINS_R = sorted(MCP_PINS, reverse=True)
SPEED_LIMIT = 10
NUM_LEDS = len(MCP_PINS)
BLINK_SPEED = 0.03

with open('/home/pi/.maker_key', 'r') as key_file:
    maker_key = key_file.read()

def main():
    for i in range(1,4):
        try:
            ping, download, upload = get_speedtest_results()
            print('Ping: {}'.format(str(ping)))
            print('Download: {}'.format(str(download)))
            print('Upload: {}'.format(str(upload)))
            maker_url = 'https://maker.ifttt.com/trigger/speedtest/with/key/' + maker_key + '?value1=' + str(ping) + '&value2=' + str(download) + '&value3=' + str(upload)
            content = requests.get(maker_url).text
            print(content)
            speedometer(download)
            os.system('sudo python /home/pi/pi-scripts/speedoled.py ' + str(download) + ' ' + str(upload))
            exit()
        except ValueError as err:
            print(err)
            print('Try {} - Trying again....'.format(str(i)))
            pass
        else:
            print('Ping: {}'.format(str(ping)))

def speedometer(speed):
    if speed > SPEED_LIMIT: speed = SPEED_LIMIT
    speed_percent = (speed * 100) / SPEED_LIMIT
    leds_lit = (NUM_LEDS * speed_percent) / 100
    leds_lit = int(math.ceil(leds_lit))
    print('LEDs lit: {}/{}'.format(str(leds_lit), str(NUM_LEDS)))
    mcp = MCP230xx.MCP23017()
    for PIN in MCP_PINS:
        mcp.setup(PIN, GPIO.OUT)
    for i in range(0, 10):
        for PIN in MCP_PINS:
            mcp.output(PIN, 1)
            time.sleep(BLINK_SPEED)
            NEXT_PIN = PIN + 1
            mcp.output(NEXT_PIN, 1)
            mcp.output(PIN, 0)
            time.sleep(BLINK_SPEED)
        for PIN in MCP_PINS_R:
            mcp.output(PIN, 1)
            time.sleep(BLINK_SPEED)
            PREV_PIN = PIN - 1
            if (PREV_PIN != -1):
                mcp.output(PREV_PIN, 1)
                mcp.output(PIN, 0)
                time.sleep(BLINK_SPEED)
    i = 1
    for PIN in MCP_PINS:
        if leds_lit >= i:
            mcp.output(PIN, 1)
            time.sleep(BLINK_SPEED)
        else:
            mcp.output(PIN, 0)
        i += 1

def get_speedtest_results():
    ping = download = upload = None 
    with os.popen('speedtest --simple') as speedtest_output:
        for line in speedtest_output:
            label, value, unit = line.split()
            if 'Ping' in label:
                ping = float(value)
            elif 'Download' in label:
                download = float(value)
            elif 'Upload' in label:
                upload = float(value)
    if all((ping, download, upload)):
        return ping, download, upload
    else:
        raise ValueError('TEST FAILED')

if __name__ == '__main__':
    main()
