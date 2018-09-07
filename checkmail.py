#!/usr/bin/sudo env/bin/python3
# *-* coding: utf-8 -*-
"""Check email periodically and notify"""

from __future__ import print_function
import httplib2
import os
import time
import multiprocessing
import RPi.GPIO as GPIO
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import ssl
try:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from http.server import BaseHTTPRequestHandler, HTTPServer

NEWMAIL_OFFSET = 0
MAIL_CHECK_FREQ = 600  # check mail every 600 seconds
PID_FILE = '/tmp/checkmail.pid'
HTTP_PORT = 26337

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
MAIL_LED = 24
BUTTON = 23
GPIO.setup(MAIL_LED, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'PiMailCheck'


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    response = service.users().messages() \
        .list(userId='me', labelIds=['INBOX', 'UNREAD']).execute()
    messages = []
    if 'messages' in response:
        messages.extend(response['messages'])
    while 'nextPageToken' in response:
        # page_token = response['nextPageToken']
        response = service.users().messages() \
            .list(userId='me', labelIds=['INBOX', 'UNREAD'], pageToken=1) \
            .execute()
        messages.extend(response['messages'])
    return(len(messages))


def check_mail():
    print('Checking gmail...')
    newmails = main()
    if newmails > NEWMAIL_OFFSET:
        print('{} new emails!'.format(newmails))
        GPIO.output(MAIL_LED, True)
    else:
        print('No new emails!')
        GPIO.output(MAIL_LED, False)


def blink_led():
    while True:
        GPIO.output(MAIL_LED, True)
        time.sleep(0.1)
        GPIO.output(MAIL_LED, False)
        time.sleep(0.1)


def error_led():
    for i in range(4):
        GPIO.output(MAIL_LED, True)
        time.sleep(1.5)
        GPIO.output(MAIL_LED, False)
        time.sleep(0.5)


def cont_check():
    with open(PID_FILE, 'w') as fh:
        fh.write(str(os.getpid()))
    while True:
        check_mail()
        time.sleep(MAIL_CHECK_FREQ)


def force_check_now():
    blink_thread = multiprocessing.Process(target=blink_led)
    blink_thread.start()
    force_check_now_thread = multiprocessing.Process(target=check_mail)
    force_check_now_thread.start()
    force_check_now_thread.join(10)
    if force_check_now_thread.is_alive():
        force_check_now_thread.terminate()
        error_led()
    blink_thread.terminate()


def force_check():
    while True:
        GPIO.wait_for_edge(BUTTON, GPIO.FALLING)
        print('Button pressed!')
        force_check_now()


class S(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('Checking mail. '.encode('utf-8'))
            webreq_check_inner_thread = multiprocessing \
                .Process(target=force_check_now)
            webreq_check_inner_thread.start()
            webreq_check_inner_thread.join()
            self.wfile.write('Done!'.encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('Page not found'.encode('utf-8'))


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
        main()
        cont_check_thread = multiprocessing.Process(target=cont_check)
        cont_check_thread.start()
        force_check_thread = multiprocessing.Process(target=force_check)
        force_check_thread.start()
        webreq_check_thread = multiprocessing.Process(target=run_server)
        webreq_check_thread.start()
    except KeyboardInterrupt:
        cont_check_thread.terminate()
        force_check_thread.terminate()
        httpd.server_close()
        webreq_check_thread.terminate()
        GPIO.cleanup()
        print('GPIO cleanup done!')
        os.remove(PID_FILE)
        print('PID file removed!')
