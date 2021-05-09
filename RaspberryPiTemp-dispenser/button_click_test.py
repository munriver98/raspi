import RPi.GPIO as gpio
from time import sleep
gpio.setmode(gpio.BCM)
gpio.setup(4,gpio.IN)
gpio.setup(17,gpio.IN)
gpio.setup(27,gpio.IN)
gpio.setup(22,gpio.IN)

try:
    while True:
        # Remember that your sentences can only be 16 characters long!
        button1=gpio.input(4)
        button2=gpio.input(17)
        button3=gpio.input(27)
        button4=gpio.input(22)
        if not button1:
            print('1')
            sleep(1)                                           # Give time for the message to be read
        elif not button2:
            print('2')
            sleep(1)                                           # Give time for the message to be read
        elif not button3:
            print('3')
            sleep(1)                                           # Give time for the message to be read
        elif not button4:
            print('4')
            sleep(1)                                           # Give time for the message to be read
except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()
