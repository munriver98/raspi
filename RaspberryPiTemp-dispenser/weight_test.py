#! /usr/bin/python2

import time
import sys



import RPi.GPIO as GPIO
from hx711 import HX711

def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()
        
    print("Bye!")
    sys.exit()

hx = HX711(20, 16)

hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(2088)

hx.reset()

hx.tare()


while True:
    try:
        val = hx.get_weight(5)
        val=round(val,4)
        if int(val)>0:
            print(val)


        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
