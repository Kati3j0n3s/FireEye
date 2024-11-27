# # Duration of LONG_PRESS in seconds
# import RPi.GPIO as GPIO

# GPIO.setmode(GPIO.BCM)
# BtnPin = 12
# LONG_PRESS = 10

# def configure_button():
  # GPIO.setup(BtnPin, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Set pin as input with pull-up resistor
  # GPIO.add_event_detect(BtnPin, GPIO.FALLING, callback = button_callback, bouncetime = 200)

# def button_callback(channel):
    # start_time = time.time()
    # while GPIO.input(BtnPin) == GPIO.LOW:
        # time.sleep(0.1) # Debouncing?

    # press_duration = time.time() - start_time

    # if press_duration >= LONG_PRESS_DURATION:
        # print("Long press detected. Resetting system...")
        # start_up_sequence(BtnPin, TempPin, HumidityPin)
    # else:
        # print("Single press detected. Running diagnostic check...")
        # diagnostic_check(BtnPin, TempPin, HumidityPin)

'''
Button Handler Take 2
The purpose of this is to allow function of the button to...
1. Short press = re-diagnose
2. Long press = reset the raspberry pi
'''

import RPi.GPIO as GPIO
import time
import os

from Diagnostic import *

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# BtnPin = 12
# START_TIME = None
# LONG_PRESS = 10

# def short_press():
    # print("Short press detected, running diagnostics")
    # diagnostic_check(BtnPin, TempPin, Humidity)

# def long_press():
    # print("Long press detected, restarting raspberry pi")
    # os.system("sudo reboot")
    
# # Event call
# def button_pressed_callback(channel):
    # global START_TIME
    # if GPIO.input(BtnPin) == GPIO.LOW
        # START_TIME = time.time()
    # else:
        # if START_TIME is not None:
            # press_duration = time.time() - START_TIME
            # START_TIME = None
            # if press_duration >= LONG_PRESS:
                # long_press()
            # else:
                # short_press()
                
class ButtonHandler:
    def __init__(self, pin, LONG_PRESS = 10):
        self.BtnPin = pin
        self.LONG_PRESS = LONG_PRESS
        self.PRESS_START = None
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BtnPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        
        GPIO.add_event_detect(self.BtnPin, GPIO.BOTH, callback = self.button_pressed_callback, bouncetime = 100)
        
    def button_pressed_callback(self, channel):
        if GPIO.input(self.BtnPin) == GPIO.LOW:
            self.PRESS_START = time.time()
        else:
            if self.PRESS_START is not None:
                press_duration = time.time() - self.PRESS_START
                self.PRESS_START = None
                if press_duration >= self.LONG_PRESS:
                    self.long_press()
                else:
                    self.short_press()

    def short_press(self):
        print("Short press detected, running diagnostics")
        diagnostic_check(BtnPin, TempPin, Humidity)

    def long_press(self):
        print("Long press detected, restarting raspberry pi")
        os.system("sudo reboot")

    def cleanup(self):
        GPIO.cleanup()
