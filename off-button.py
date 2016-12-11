import RPi.GPIO as GPIO
import os

PIN=22

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    GPIO.wait_for_edge(PIN, GPIO.FALLING)
    print('Let\'s shut down this beast.')
    os.system('sudo shutdown -h now')
except:
    pass

GPIO.cleanup()
