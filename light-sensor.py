from __future__ import print_function
import requests
import wiringpi
import time

PIN_BASE = 65
I2C_ADDR = 0x20
MCP_PIN = 80

wiringpi.wiringPiSetup()
wiringpi.mcp23017Setup(PIN_BASE, I2C_ADDR)

with open('/home/pi/.maker_key', 'r') as key_file:
    maker_key = key_file.read()

def rc_time (MCP_PIN):
    count = 0
    wiringpi.pinMode(MCP_PIN, 1)
    wiringpi.digitalWrite(MCP_PIN, 0)
    time.sleep(0.1)
    wiringpi.pinMode(MCP_PIN, 0)
    while (wiringpi.digitalRead(MCP_PIN) == 0):
        count += 1
    return count

if __name__ == '__main__':
    light_level = rc_time(MCP_PIN)
    print('Light Level: {}'.format(str(light_level)))
    maker_url = 'https://maker.ifttt.com/trigger/light-sensor/with/key/' + maker_key + '?value1=' + str(light_level)
    content = requests.get(maker_url).text
    print(content)
