import os
import urllib2
import wiringpi
import math
import time

PIN_BASE = 65
I2C_ADDR = 0x20
MCP_PINS = [65, 66, 67, 68, 69, 70, 71, 72, 73, 74]
SPEED_LIMIT = 10
NUM_LEDS = len(MCP_PINS)
BLINK_SPEED = 0.03

with open("/home/pi/.maker_key", "r") as key_file:
    maker_key = key_file.read()

def main():
    for i in range(1,4):
        try:
            ping, download, upload = get_speedtest_results()
            print('Ping: ' + str(ping))
            print('Download: ' + str(download))
            print('Upload: ' + str(upload))
            maker_url = "https://maker.ifttt.com/trigger/speedtest/with/key/" + maker_key + "?value1=" + str(ping) + "&value2=" + str(download) + "&value3=" + str(upload)
            content = urllib2.urlopen(maker_url).read()
            print(content)
            speedometer(download)
            exit()
        except ValueError as err:
            print(err)
            print('Try ' + str(i) + ' - Trying again....')
            pass
        else:
            print('Ping: ' + str(ping))

def speedometer(speed):
    if speed > SPEED_LIMIT: speed = SPEED_LIMIT
    speed_percent = (speed * 100) / SPEED_LIMIT
    leds_lit = (NUM_LEDS * speed_percent) / 100
    leds_lit = int(math.ceil(leds_lit))
    print('LEDs lit: ' + str(leds_lit) + '/' + str(NUM_LEDS))
    wiringpi.wiringPiSetup()
    wiringpi.mcp23017Setup(PIN_BASE,I2C_ADDR)
    for PIN in MCP_PINS:
        wiringpi.pinMode(PIN, 1)
    for i in range(0, 10):
        for PIN in MCP_PINS:
            wiringpi.digitalWrite(PIN, 1)
            time.sleep(BLINK_SPEED)
            NEXT_PIN = PIN + 1
            wiringpi.digitalWrite(NEXT_PIN, 1)
            wiringpi.digitalWrite(PIN, 0)
            time.sleep(BLINK_SPEED)
    i = 1
    for PIN in MCP_PINS:
        if leds_lit >= i:
            wiringpi.digitalWrite(PIN, 1)
        else:
            wiringpi.digitalWrite(PIN, 0)
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
