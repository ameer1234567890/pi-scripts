#!/usr/bin/sudo env/bin/python3
# *-* coding: utf-8 -*-
"""Check and alert of door movement"""

from __future__ import print_function 
import RPi.GPIO as GPIO
import os
import time
import datetime
import multiprocessing
import requests
import ssl
try:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from http.server import BaseHTTPRequestHandler, HTTPServer

SENSOR_PIN = 14
LED_PIN = 15
STATE_FILE = 'door.state'
READ_STATE_INTERVAL = 10
PID_FILE = '/tmp/door.pid'
HTTP_PORT = 26339
MAKER_BASE_URL = 'https://maker.ifttt.com/trigger/door/with/key/'

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

with open('/home/pi/.maker_key', 'r') as key_file:
    maker_key = key_file.read()

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


def check_door():
    try:
        while 1:
            with open(STATE_FILE, 'r') as fh:
                state = fh.read()
            if state == '1':
                GPIO.wait_for_edge(SENSOR_PIN, GPIO.RISING)
                print('Door movement at {}'.format(datetime.datetime.now()))
                maker_url = MAKER_BASE_URL + maker_key
                content = requests.get(maker_url).text
                print(content)
                time.sleep(1)
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
    def do_GET(self):
        if self.path == '/on':
            self.send_response(200)
            self.send_header('Contecnt-type', 'text/html')
            self.end_headers()
            self.wfile.write('<html><body><p>Arming door sensor...'
                             .encode('utf-8'))
            webreq_check_inner_thread = multiprocessing. \
                Process(target=arm_sensor)
            webreq_check_inner_thread.start()
            webreq_check_inner_thread.join()
            self.wfile.write('Done!</p></body></html>'.encode('utf-8'))
        elif self.path == '/off':
            self.send_response(200)
            self.send_header('Contecnt-type', 'text/html')
            self.end_headers()
            self.wfile.write('<html><body><p>Disarming door sensor...'
                             .encode('utf-8'))
            webreq_check_inner_thread = multiprocessing \
                .Process(target=disarm_sensor)
            webreq_check_inner_thread.start()
            webreq_check_inner_thread.join()
            self.wfile.write('Done!</p></body></html>'.encode('utf-8'))
        elif self.path == '/status':
            self.send_response(200)
            self.send_header('Contecnt-type', 'text/html')
            self.end_headers()
            self.wfile.write('<html><body><p>'.encode('utf-8'))
            with open(STATE_FILE, 'r') as fh:
                state = fh.read()
            if state == '1':
                self.wfile.write('Armed'.encode('utf-8'))
            else:
                self.wfile.write('Disarmed'.encode('utf-8'))
            self.wfile.write('</p></body></html>'.encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Contecnt-type', 'text/html')
            self.end_headers()
            self.wfile.write('<html><body><p>Page not found</p></body></html>'
                             .encode('utf-8'))


def run_server(server_class=HTTPServer, handler_class=S, port=HTTP_PORT):
    server_address = ('', port)
    global httpd
    httpd = server_class(server_address, handler_class)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='../tls/rpi1.pem',
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
