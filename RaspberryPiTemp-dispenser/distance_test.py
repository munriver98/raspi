#! /usr/bin/env python

# Simple string program. Writes and updates strings.
# Demo program for the I2C 16x2 Display from Ryanteck.uk
# Created by Matthew Timmons-Brown for The Raspberry Pi Guy YouTube channel

# Import necessary libraries for communication and display use
import drivers
from time import sleep
import time
import smbus			#import SMBus module of I2C
import RPi.GPIO as gpio
import threading
# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first
trig=10
echo=9
gpio.setmode(gpio.BCM)
gpio.setup(trig,gpio.OUT)
gpio.setup(echo,gpio.IN)



def get_distance():
    global echo,trig
    try:

        while True:#trig= 9 echo =10
            gpio.output(trig,False)
            sleep(0.5)

            gpio.output(trig,True)
            sleep(0.00001)
            gpio.output(trig,False)
            while gpio.input(echo)==0:
                pulse_start=time.time()
            while gpio.input(echo)==1:
                pulse_end=time.time()
            pulse_duration=pulse_end-pulse_start
            distance=pulse_duration*17000
            distance=round(distance,2)
            print(distance)
    except:
        print('break get distance')
        gpio.cleanup()
get_distance()
