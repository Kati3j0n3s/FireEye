

# Importing Libraries
import RPi.GPIO as GPIO
import PCF8591 as ADC   # Not needed yet, but I think I do....
import time

# Referencing the other py files
from StartUpSequence import *
from Diagnostic import *
from ButtonHandler import ButtonHandler
from UsingAllSensors import *

# Configures GPIO to use Broadcom chip numbering scheme.
GPIO.setmode(GPIO.BCM)

# Configuring Pins
BtnPin = 18
TempPin = 7
HumidityPin = 16

db18b20 = ''

# Sets up the sensors.
def setup():
  GPIO.setup(BtnPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
  GPIO.setup(TempPin, GPIO.IN)
  GPIO.setup(HumidityPin, GPIO.IN)

# Start up sequence
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
  GPIO.cleanup()

  try:
    setup()
    start_up()
    # For now, cause it's dumb, giving up on button implementation
    # button_handler = ButtonHandler(pin = BtnPin, LONG_PRESS = 10)
    
    # Temp testing
    # data()
    time.sleep(1) # Keeps looping to keep program alive

  except KeyboardInterrupt:
    print("Exiting Program")
    
  finally:
    button_handler.cleanup()
    GPIO.cleanup()
