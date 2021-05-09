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
import pygame
# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first

def play_music(name):
    path='./'
    pygame.mixer.init()
    pygame.mixer.music.load(path+name)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy()==True:
        continue

play_music('breakfast.mp3')
