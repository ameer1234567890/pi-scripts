import RPi.GPIO as GPIO
import os

gpio_pin_number=22

GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    GPIO.wait_for_edge(gpio_pin_number, GPIO.FALLING)
    print('Let\'s shut down this beast.')
    os.system("sudo shutdown -h now")
except:
    pass

GPIO.cleanup()
