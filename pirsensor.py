import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

LED = 8
BUZZER = 11
GPIO_PIR = 9

GPIO.setup(LED, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)

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
            print('Warning, I\'ve detected a movement for {} time(s)'.format(num))
            GPIO.output(LED, True)
            GPIO.output(BUZZER, True)
            time.sleep(0.2)
            GPIO.output(BUZZER, False)
            status1 = 1
        elif status0 == 0 and status1 == 1:
            print('Ready to start!')
            GPIO.output(LED, False)
            status1 = 0
        time.sleep(0.01)
except KeyboardInterrupt:
    print('Exit!')
    GPIO.cleanup()
