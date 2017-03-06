import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

LED_ONE = 8
LED_TWO = 11
GPIO_PIR = 9

GPIO.setup(LED_ONE, GPIO.OUT)
GPIO.setup(LED_TWO, GPIO.OUT)

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
            GPIO.output(LED_ONE, True)
            GPIO.output(LED_TWO, True)
            status1 = 1
        elif status0 == 0 and status1 == 1:
            print('Ready to start!')
            GPIO.output(LED_ONE, False)
            GPIO.output(LED_TWO, False)
            status1 = 0
        time.sleep(0.01)
except KeyboardInterrupt:
    print('Exit!')
    GPIO.cleanup()
