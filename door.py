#!/usr/bin/sudo env/bin/python3
# *-* coding: utf-8 -*-
"""Turn on light when door opens and off when door closes"""

from __future__ import print_function
import RPi.GPIO as GPIO
import os
import time
import multiprocessing
import ssl
import smbus
import yeelight
try:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from http.server import BaseHTTPRequestHandler, HTTPServer

BULB_IP = "192.168.7.190"
SENSOR_PIN = 14
LED_PIN = 15
STATE_FILE = 'door.state'
READ_STATE_INTERVAL = 10
KEEP_ON_FOR = 7
PID_FILE = '/tmp/door.pid'
HTTP_PORT = 7400

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
bulb = yeelight.Bulb(BULB_IP)

# bh1750 Light Sensor code picked from https://bitbucket.org/ \
# MattHawkinsUK/rpispy-misc/raw/master/python/bh1750.py
DEVICE = 0x23
POWER_DOWN = 0x00
POWER_ON = 0x01
RESET = 0x07
CONTINUOUS_LOW_RES_MODE = 0x13
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
ONE_TIME_HIGH_RES_MODE_1 = 0x20
ONE_TIME_HIGH_RES_MODE_2 = 0x21
ONE_TIME_LOW_RES_MODE = 0x23

bus = smbus.SMBus(1)

with open(PID_FILE, 'w') as fh:
    fh.write(str(os.getpid()))

if not os.path.isfile(STATE_FILE):
    with open(STATE_FILE, 'w') as fh:
        fh.write('1')
        GPIO.output(LED_PIN, 1)

with open(STATE_FILE, 'r') as fh:
    state = fh.read()

if state == '1':
    GPIO.output(LED_PIN, 1)
else:
    GPIO.output(LED_PIN, 0)


def convert_to_number(data):
    result = (data[1] + (256 * data[0])) / 1.2
    return (result)


def read_light(addr=DEVICE):
    data = bus.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE_1)
    return convert_to_number(data)


def check_door():
    try:
        while 1:
            with open(STATE_FILE, 'r') as fh:
                state = fh.read()
            if state == '1':
                GPIO.wait_for_edge(SENSOR_PIN, GPIO.FALLING)
                print('Door opened')
                # Read and sleep for 0.2 seconds to calibrate sensor,
                # then read real value
                read_light()
                time.sleep(0.2)
                light_level = read_light()
                if light_level < 1:
                    print('Turning on LED strip... Light level: {}'
                          .format(light_level))
                    bulb.turn_on()
                    GPIO.wait_for_edge(SENSOR_PIN, GPIO.RISING)
                    print('Door closed')
                    time.sleep(KEEP_ON_FOR)
                    bulb.turn_off()
                    print('Light turned off')
                else:
                    print('There is already light! Light level: {}'
                          .format(light_level))
            elif state == '0':
                time.sleep(READ_STATE_INTERVAL)
            else:
                print('Error: State file in unknown state!')
                break
    except:  # noqa: E722
        pass


def arm_sensor():
    with open(STATE_FILE, 'w') as fh:
        fh.write('1')
    GPIO.output(LED_PIN, 1)


def disarm_sensor():
    with open(STATE_FILE, 'w') as fh:
        fh.write('0')
    GPIO.output(LED_PIN, 0)


class S(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        if self.path == '/on':
            self.send_response(302)
            webreq_check_inner_thread = multiprocessing \
                .Process(target=arm_sensor)
            webreq_check_inner_thread.start()
            webreq_check_inner_thread.join()
            self.send_header('Location', '/')
            self.end_headers()
        elif self.path == '/off':
            self.send_response(302)
            webreq_check_inner_thread = multiprocessing \
                .Process(target=disarm_sensor)
            webreq_check_inner_thread.start()
            webreq_check_inner_thread.join()
            self.send_header('Location', '/')
            self.end_headers()
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Contecnt-type', 'text/html')
            self.end_headers()
            self.wfile.write('<html><head><meta name="viewport" '
                             'content="width=device-width, initial-scale=1">'
                             '<style>a{padding:40px 40px;text-decoration:'
                             'none;text-transform:uppercase;text-align:'
                             'center;font-family:monospace;display:block;'
                             'width:5em;}a.armed{background:red;color:white;}'
                             'a.disarmed{background:green;color:white;}'
                             '</style></head><body><p>'.encode('utf-8'))
            with open(STATE_FILE, 'r') as fh:
                state = fh.read()
            if state == '1':
                self.wfile.write('<a class="armed" href="/off">Armed</a>'
                                 .encode('utf-8'))
            else:
                self.wfile.write('<a class="disarmed" href="/on">Disarmed</a>'
                                 .encode('utf-8'))
            self.wfile.write('</p></body></html>'.encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Contecnt-type', 'text/html')
            self.end_headers()
            self.wfile.write('<html><body><p>Page not found. <a href="/">'
                             'Check status of PIR sensor</a></p></body></html>'
                             .encode('utf-8'))


def run_server(server_class=HTTPServer, handler_class=S, port=HTTP_PORT):
    server_address = ('', port)
    global httpd
    httpd = server_class(server_address, handler_class)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='../tls/device.pem',
                                   server_side=True)
    print('Starting httpd...')
    httpd.serve_forever()


if __name__ == '__main__':
    try:
        check_door_thread = multiprocessing.Process(target=check_door)
        check_door_thread.start()
        run_server_thread = multiprocessing.Process(target=run_server)
        run_server_thread.start()
    except KeyboardInterrupt:
        check_door_thread.terminate()
        httpd.server_close()
        run_server_thread.terminate()
        GPIO.cleanup()
        print('GPIO cleanup done!')
        os.remove(PID_FILE)
        print('PID file removed!')
