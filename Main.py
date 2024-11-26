

# Importing Libraries
import RPi.GPIO as GPIO
import PCF8591 as ADC   # Not needed yet, but I think I do....
import time

# Referencing the other py files
from StartUpSequence import *
from Diagnostic import *
from ButtonHandler import *
from UsingAllSensors import *

# Configures GPIO to use Broadcom chip numbering scheme.
GPIO.setmode(GPIO.BCM)
BtnPin = 12
TempPin = 7
HumidityPin = 16

db18b20 = ''

# Sets up the sensors.
def setup():
  GPIO.setup(BtnPin, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Probably need to change PUD_UP
  GPIO.setup(TempPin, GPIO.IN)
  GPIO.setup(HumidityPin, GPIO.IN)
  

'''
When called, it will run once for the initial diagnostic before continuing on.

NOTE: I'll add it here, but it may be beneficial to have it in its own file.
'''
def start_up():
  # Run diagnostic_check()
  # If it gives back failed, indicate what failed via screen and light
  # NOTE: Will need to add that logic within diagnostic_check().
  # Wait until diagnostic has been run (or reset) and has given a success
  # If success then green light then....
  # Run battery life check -> separate file as well cause that will be it's own issues
  # If battery life is greater than 20 minutes (may need a percentage) continue on
  # Else give warning of battery life and do not continue on.
  
  diagnostic_check(BtnPin, TempPin, HumidityPin)


if __name__ == "__main__":

  try:
    setup()
    start_up()
    data()
    time.sleep(1) # Keeps looping to keep program alive

  except KeyboardInterrupt:
    GPIO.cleanup()
