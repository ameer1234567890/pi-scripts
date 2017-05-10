from __future__ import print_function
import time
import RPi.GPIO as GPIO
import os
import multiprocessing
import requests
try:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from http.server import BaseHTTPRequestHandler, HTTPServer

GPIO.setmode(GPIO.BCM)

STATE_LED = 8
BUZZER = 11
GPIO_PIR = 9
STATE_FILE = 'pirsensor.state'
PID_FILE = '/tmp/pirsensor.pid'
HTTP_PORT = 7000
NOTIFY_INTERVAL = 30
LOG_FILE = 'pirsensor.log'
MY_PHONE_HOSTNAME = 'nexus5x.lan'


GPIO.setup(STATE_LED, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)

with open('/home/pi/.maker_key', 'r') as key_file:
    maker_key = key_file.read()

if os.path.isfile(LOG_FILE) == False:
    with open(LOG_FILE, 'w') as fh:
        fh.write('%s' % time.time())

with open(PID_FILE, 'w') as fh:
    fh.write(str(os.getpid()))

if os.path.isfile(STATE_FILE) == False:
    with open(STATE_FILE, 'w') as fh:
        fh.write('1')
        GPIO.output(STATE_LED, 1)

with open(STATE_FILE, 'r') as fh:
    state = fh.read()

if state == '1':
    GPIO.output(STATE_LED, 1)
else:
    GPIO.output(STATE_LED, 0)

def check_pir():
    print('PIR Sensor is running! (CTRL+C to exit)')
    GPIO.setup(GPIO_PIR, GPIO.IN)
    num = 0
    status0 = 0
    status1 = 0  
    try:
        print('Waiting for our sensor...')
        while GPIO.input(GPIO_PIR) == 1:
            status0 = 0
        print('Ready to start!')
        while True:
            status0 = GPIO.input(GPIO_PIR)
            if status0 == 1 and status1 == 0:
                num = num + 1
                with open(STATE_FILE, 'r') as fh:
                    state = fh.read()
                if state == '1':
                    print('Movement detected for {} time(s)'.format(num))
                    GPIO.output(BUZZER, True)
                    time.sleep(0.2)
                    GPIO.output(BUZZER, False)
                    time_now = time.time()
                    with open(LOG_FILE, 'r') as fh:
                        time_last_notif = float(fh.read())
                    if time_now > time_last_notif + NOTIFY_INTERVAL:
                        response = os.system("ping -c 1 " + MY_PHONE_HOSTNAME)
                        if response == 0:
                            print('Not notifying since you are home!')
                        else:
                            print('Notifying about movement')
                            maker_url = 'https://maker.ifttt.com/trigger/pir-movement/with/key/' + maker_key
                            content = requests.get(maker_url).text
                            print(content)
                            with open(LOG_FILE, 'w') as fh:
                                fh.write('%s' % time.time())
                    else:
                        print('Not notifying yet!')
                else:
                    print('Movement detected for {} time(s) but sensor is unarmed!'.format(num))
                status1 = 1
            elif status0 == 0 and status1 == 1:
                print('Ready to start!')
                status1 = 0
            time.sleep(0.01)
    except KeyboardInterrupt:
        print('Exit!')
        GPIO.cleanup()

def arm_sensor():
    with open(STATE_FILE, 'w') as fh:
        fh.write('1')
    GPIO.output(STATE_LED, 1)

def disarm_sensor():
    with open(STATE_FILE, 'w') as fh:
        fh.write('0')
    GPIO.output(STATE_LED, 0)

class S(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/on':
            self.send_response(302)
            webreq_check_inner_thread = multiprocessing.Process(target=arm_sensor)
            webreq_check_inner_thread.start()
            webreq_check_inner_thread.join()
            self.send_header('Location', '/')
            self.end_headers()
        elif self.path == '/off':
            self.send_response(302)
            webreq_check_inner_thread = multiprocessing.Process(target=disarm_sensor)
            webreq_check_inner_thread.start()
            webreq_check_inner_thread.join()
            self.send_header('Location', '/')
            self.end_headers()
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Contecnt-type', 'text/html')
            self.end_headers()
            self.wfile.write('<html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>a{padding:40px 40px;text-decoration:none;text-transform:uppercase;text-align:center;font-family:monospace;display:block;width:5em;}a.armed{background:red;color:white;}a.disarmed{background:green;color:white;}</style></head><body><p>'.encode('utf-8'))
            with open(STATE_FILE, 'r') as fh:
                state = fh.read()
            if state == '1':
                self.wfile.write('<a class="armed" href="/off">Armed</a>'.encode('utf-8'))
            else:
                self.wfile.write('<a class="disarmed" href="/on">Disarmed</a>'.encode('utf-8'))
            self.wfile.write('</p></body></html>'.encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Contecnt-type', 'text/html')
            self.end_headers()
            self.wfile.write('<html><body><p>Page not found. <a href="/">Check status of PIR sensor</a></p></body></html>'.encode('utf-8'))

def run_server(server_class=HTTPServer, handler_class=S, port=HTTP_PORT):
    server_address = ('', port)
    global httpd
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == '__main__':
    try:
        check_pir_thread = multiprocessing.Process(target=check_pir)
        check_pir_thread.start()
        run_server_thread = multiprocessing.Process(target=run_server)
        run_server_thread.start()
    except KeyboardInterrupt:
        check_pir_thread.terminate()
        httpd.server_close()
        run_server_thread.terminate()
        GPIO.cleanup()
        print('GPIO cleanup done!')
        os.remove(PID_FILE)
        print('PID file removed!')
