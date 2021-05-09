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
from hx711 import HX711
import math
from datetime import datetime
# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first
display = drivers.Lcd()
up_btn=4
down_btn=22
ok_btn=27
reset_btn=17
breakfast_servo=14 
lunch_servo=15 
dinner_servo=18
SERVO_MAX_DUTY=12
SERVO_MIN_DUTY=3
piezo=11
trig=10
echo=9
gpio.setmode(gpio.BCM)
gpio.setup(up_btn,gpio.IN)
gpio.setup(down_btn,gpio.IN)
gpio.setup(ok_btn,gpio.IN)
gpio.setup(reset_btn,gpio.IN)
gpio.setup(breakfast_servo,gpio.OUT)
gpio.setup(lunch_servo,gpio.OUT)
gpio.setup(dinner_servo,gpio.OUT)
gpio.setup(trig,gpio.OUT)
gpio.setup(piezo,gpio.OUT)
gpio.setup(echo,gpio.IN)

gpio.output(piezo,False)

s1=gpio.PWM(breakfast_servo,50)
s2=gpio.PWM(lunch_servo,50)
s3=gpio.PWM(dinner_servo,50)
play_piezo=True
s1.start(0)
s2.start(0)
s3.start(0)


# Dfrobot SEN0160 Digital Weight Sensor
hx=HX711(20,16)
hx.set_reading_format("MSB","MSB")
hx.set_reference_unit(2088)
hx.reset()
hx.tare()

def setServoPos(servo,degree):
    global s1
    if degree>180:
        degree=180
    if degree==0:
        servo.ChangeDutyCycle(0)
    else:
        duty=SERVO_MIN_DUTY+(degree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/180.0)
        servo.ChangeDutyCycle(duty)
     
# setServoPos(s1,90)
# sleep(1)
# setServoPos(s1,180)
# sleep(1)
# setServoPos(s2,90)
# sleep(1)
# setServoPos(s2,180)
# sleep(1)
# setServoPos(s3,110)
# sleep(1)
# setServoPos(s3,20)
# sleep(1)
setServoPos(s1,0)
setServoPos(s2,0)
setServoPos(s3,0)
#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

def MPU_Init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value


bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address
breakfast_time=0
lunch_time=0
dinner_time=0
MPU_Init()
def init_meal_time():
    with open('./setmealtime.txt','w') as f:
        f.write('init')
        print('init meal_time_file')
def get_meal_time():
    global breakfast_time,lunch_time,dinner_time
    line=''
    with open('./setmealtime.txt','r') as f:
        line=f.readline()
        strs=line.split(' ')
        breakfast_time=int(strs[1])
        lunch_time=int(strs[2])
        dinner_time=int(strs[3])
        print(line)
    if "set" in line:
        return True
    else:
        return False
def set_meal_time():
        with open('./setmealtime.txt','w') as f:
            f.write('set')
        print('set breakfast time')
        t=0
        display.lcd_display_string("set breakfast time", 1)  # Write line of text to second line of display
        while True:
            up_=gpio.input(up_btn)
            down_=gpio.input(down_btn)
            ok_=gpio.input(ok_btn)
            if not up_:
                t=t+1
                display.lcd_display_string(str(t), 2)  # Write line of text to second line of display
                sleep(1)
            elif not down_:
                if t>0:
                    t=t-1
                    display.lcd_display_string(str(t), 2)  # Write line of text to second line of display
                    sleep(1)
            elif not ok_:
                print('set breakfast time is : {} minutes after'.format(t))
                display.lcd_display_string('breakfast {}m after'.format(t), 2)  # Write line of text to second line of display
                sleep(2)
                display.lcd_clear()                                # Clear the display of any data
                with open('./setmealtime.txt','a') as f:
                    f.write(' '+str(t))
                break
        t=0
        display.lcd_display_string("set lunch time  ", 1)  # Write line of text to second line of display
        while True:
            up_=gpio.input(up_btn)
            down_=gpio.input(down_btn)
            ok_=gpio.input(ok_btn)
            if not up_:
                t=t+1
                display.lcd_display_string(str(t), 2)  # Write line of text to second line of display
                sleep(1)
            elif not down_:
                if t>0:
                    t=t-1
                    display.lcd_display_string(str(t), 2)  # Write line of text to second line of display
                    sleep(1)
            elif not ok_:
                print('lunch is : {} minutes after'.format(t))
                display.lcd_display_string('lunch {} m after'.format(t), 2)  # Write line of text to second line of display
                sleep(2)
                display.lcd_clear()                                # Clear the display of any data
                with open('./setmealtime.txt','a') as f:
                    f.write(' '+str(t))
                break
        t=0
        display.lcd_display_string("set dinner time", 1)  # Write line of text to second line of display
        while True:
            up_=gpio.input(up_btn)
            down_=gpio.input(down_btn)
            ok_=gpio.input(ok_btn)
            if not up_:
                t=t+1
                display.lcd_display_string(str(t), 2)  # Write line of text to second line of display
                sleep(1)
            elif not down_:
                if t>0:
                    t=t-1
                    display.lcd_display_string(str(t), 2)  # Write line of text to second line of display
                    sleep(1)
            elif not ok_:
                print('dinner is : {} minutes after'.format(t))
                display.lcd_display_string('dinner {} m after'.format(t), 2)  # Write line of text to second line of display
                sleep(2)
                display.lcd_clear()                                # Clear the display of any data
                with open('./setmealtime.txt','a') as f:
                    f.write(' '+str(t))
                break
if get_meal_time():
    print('already set time')
else:
    set_meal_time()


distance=0
def get_distance():
    global echo,trig,distance
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

def play_piezo():
    global distance,play_piezo
    while True:
        if int(distance)<60 and int(distance) >5 and play_piezo:
            gpio.output(piezo,True)
            sleep((distance/100))
            gpio.output(piezo,False)
            sleep((distance/100))
            print('piezo')
        else:
            gpio.output(piezo,False)

t=threading.Thread(target=get_distance,daemon=True)
t.start()

t2=threading.Thread(target=play_piezo,daemon=True)
t2.start()

def monitoring_slipped():
    global display
    while True:
        acc_z = read_raw_data(ACCEL_ZOUT_H)
        Az = acc_z/16384.0
        if Az>0.5:
            print("normal")
            #display.lcd_display_string("normal", 1)  # Write line of text to first line of display
        else:
            print("slipped")
            #display.lcd_display_string("slipped", 1)  # Write line of text to first line of display
            play_music('slipped.mp3')
        sleep(0.3)
t2=threading.Thread(target=monitoring_slipped,daemon=True)
t2.start()

def play_music(name):
    path='./'
    pygame.mixer.init()
    pygame.mixer.music.load(path+name)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy()==True:
        continue

temp_time=time.time()

# Main body of code
reset=0
wait_minute=20
try:
    while True:
        # Remember that your sentences can only be 16 characters long!
        now=time.time()
        up_=gpio.input(up_btn)
        down_=gpio.input(down_btn)
        if up_==False and down_ == False:#if up and down button pushed same time than reset 
            print('reset ...')
            sleep(0.2)
            init_meal_time()
            set_meal_time()
            temp_time=time.time()
            reset=0

        check_time=int(now-temp_time)
        if reset==0 and check_time>(breakfast_time*wait_minute):
            print('breakfast time')#141518 servopin
            play_piezo=False
            t2=threading.Thread(target=play_music,args=('breakfast.mp3',),daemon=True)
            t2.start()
            setServoPos(s1,90)
            sleep(2)
            setServoPos(s1,180)
            sleep(2)
            setServoPos(s1,0)
            
            temp_weight=0
            meal_time_count=0
            start_time=time.time()
            last_time=0
            display.lcd_display_string('breakfast time!!',1)  
            while True:
                try:
                    val=hx.get_weight(5)
                    val=round(val,4)
                    val = int(val)
                    if int(val)>0:
                        print(val)
                    hx.power_down()
                    hx.power_up()
                    messages='weight :'+str(val)
                    display.lcd_display_string(messages,2)  
                    if abs(temp_weight-val)>10:
                        temp_weight=int(val)
                    else:
                        sleep(1)
                        print('nothing changed')
                        meal_time_count=meal_time_count+1
                    if meal_time_count>10:
                        print('done breakfast')
                        print('last weight is {}'.format(str(val)))
                        last_time=time.time()
                        break
                    sleep(0.1)
                except (KeyboardInterrupt,SystemExit):
                    print("Cleaning up!")
                    s1.stop()
                    s2.stop()
                    s3.stop()
                    gpio.cleanup()
                    display.lcd_clear()
            final_time=int(last_time-start_time)
            print('eatting time : {}'.format(final_time))
            messages='meal time '+str(final_time)
            
            with open('./mealdata.txt','a') as f:
                f.write(str(datetime.now().date())+'\n')
                f.write(str(datetime.now().time())+'\n')
                f.write('breakfast: '+str(val)+'\n')
                f.write('eat time: '+str(final_time-19)+'\n')
                f.write('\n')
            display.lcd_display_string(messages,3)  
            sleep(5)
            display.lcd_clear()
            sleep(1)
            play_piezo=True
            reset=1
        elif reset==1 and check_time>(lunch_time*wait_minute):
            print('lunch time')
            play_piezo=False
            t2=threading.Thread(target=play_music,args=('lunch.mp3',),daemon=True)
            t2.start()
            setServoPos(s2,90)
            sleep(2)
            setServoPos(s2,180)
            sleep(2)
            setServoPos(s2,0)
            
            
            temp_weight=0
            meal_time_count=0
            start_time=time.time()
            last_time=0
            display.lcd_display_string('lunch time!!',1)  
            while True:
                try:
                    val=hx.get_weight(5)
                    val=round(val,4)
                    val = int(val)
                    if int(val)>0:
                        print(val)
                    hx.power_down()
                    hx.power_up()
                    messages='weight :'+str(val)
                    display.lcd_display_string(messages,2)  
                    if abs(temp_weight-val)>10:
                        temp_weight=val
                    else:
                        sleep(1)
                        print('nothing changed')
                        meal_time_count=meal_time_count+1
                    if meal_time_count>10:
                        print('done lunch')
                        print('last weight is {}'.format(str(val)))
                        last_time=time.time()
                        break
                    sleep(0.1)
                except (KeyboardInterrupt,SystemExit):
                    print("Cleaning up!")
                    s1.stop()
                    s2.stop()
                    s3.stop()
                    gpio.cleanup()
                    display.lcd_clear()
            final_time=int(last_time-start_time)
            print('eatting time : {}'.format(final_time))
            messages='meal time '+str(final_time)
            with open('./mealdata.txt','a') as f:
                f.write(str(datetime.now().date())+'\n')
                f.write(str(datetime.now().time())+'\n')
                f.write('lunch: '+str(val)+'\n')
                f.write('eat time: '+str(final_time-19)+'\n')
                f.write('\n')
            display.lcd_display_string(messages,3)  
            sleep(5)
            display.lcd_clear()
            sleep(1)
            
            
            play_piezo=True
            reset=2
        elif reset==2 and check_time>(dinner_time*wait_minute):
            print('dinner time')
            play_piezo=False
            t2=threading.Thread(target=play_music,args=('dinner.mp3',),daemon=True)
            t2.start()
            setServoPos(s3,110)
            sleep(2)
            setServoPos(s3,20)
            sleep(2)
            setServoPos(s3,0)
            
            
            temp_weight=0
            meal_time_count=0
            start_time=time.time()
            last_time=0
            display.lcd_display_string('dinner time!!',1)  
            while True:
                try:
                    val=hx.get_weight(5)
                    val=round(val,4)
                    val = int(val)
                    if int(val)>0:
                        print(val)
                    hx.power_down()
                    hx.power_up()
                    messages='weight :'+str(val)
                    display.lcd_display_string(messages,2)  
                    if abs(temp_weight-val)>10:
                        temp_weight=val
                    else:
                        sleep(1)
                        print('nothing changed')
                        meal_time_count=meal_time_count+1
                    if meal_time_count>10:
                        print('done dinner')
                        print('last weight is {}'.format(str(val)))
                        last_time=time.time()
                        break
                    sleep(0.1)
                except (KeyboardInterrupt,SystemExit):
                    print("Cleaning up!")
                    s1.stop()
                    s2.stop()
                    s3.stop()
                    gpio.cleanup()
                    display.lcd_clear()
            final_time=int(last_time-start_time)
            print('eatting time : {}'.format(final_time))
            messages='meal time '+str(final_time)
            with open('./mealdata.txt','a') as f:
                f.write(str(datetime.now().date())+'\n')
                f.write(str(datetime.now().time())+'\n')
                f.write('dinner: '+str(val)+'\n')
                f.write('eat time: '+str(final_time-19)+'\n')
                f.write('\n')
            display.lcd_display_string(messages,3)  
            sleep(5)
            display.lcd_clear()
            sleep(1)
            
            temp_time=time.time()
            play_piezo=True
            reset=0
        sleep(0.1)
except KeyboardInterrupt:
    print("Cleaning up!")
    s1.stop()
    s2.stop()
    s3.stop()
    gpio.cleanup()
    display.lcd_clear()

