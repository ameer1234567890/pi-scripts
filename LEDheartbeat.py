#! /usr/bin/python
# coding: utf8
"""
Using GPIO port 7 (pin 26) on RasPi model B
GPIO7----|R330|----LED----GND
"""
import time
import RPi.GPIO as GPIO
gPin = 7
heartBeatArray = [0.05, 0.1, 0.015, 1.1] #specify here the beat timings (seconds)
tempo = 0.05 #change this to change the heartbeat tempo
hbeatIndex = 1 #need to make sure we start with the LED off
led = False #initialise LED boolean
tm_old = time.time() #initialise tm_old to be equal to current time
#setup GPIO ports to control LED
GPIO.setwarnings(False) #only needed if you have more then one instance using GPIO running 
GPIO.setmode(GPIO.BCM) #using RasPi model B here
#GPIO.setmode(GPIO.BOARD) #if you want to refer to 
#the effective pin numbers on the board's connector
GPIO.setup(gPin, GPIO.OUT)
GPIO.output(gPin, False)
#main thread
while True:
   try:
      tm_now = time.time()
      if (float(tm_now - tm_old) > (heartBeatArray[hbeatIndex] + tempo)):
         led = not led
         GPIO.output(gPin, led)
         tm_old = time.time()
         hbeatIndex += 1
      if (hbeatIndex > 3):
         hbeatIndex = 0
   
   except KeyboardInterrupt:
      break
GPIO.cleanup() #when exiting make sure you stop using GPIO
print "GPIO cleanup done"
