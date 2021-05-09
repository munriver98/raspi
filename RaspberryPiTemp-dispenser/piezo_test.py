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
piezo=11
gpio.setmode(gpio.BCM)
gpio.setup(piezo,gpio.OUT)

gpio.output(piezo,False)


def play_piezo():
    while True:
            gpio.output(piezo,True)
            sleep(1000)
            gpio.output(piezo,False)
            sleep(1000)
            print('piezo')
        else:
            gpio.output(piezo,False)

try:
    while True:
        gpio.output(piezo,True)
        sleep(1000)
        gpio.output(piezo,False)
        sleep(1000)
        except KeyboardInterrupt:
    print("Cleaning up!")
    s1.stop()
    s2.stop()
    s3.stop()
    gpio.cleanup()
    display.lcd_clear()

