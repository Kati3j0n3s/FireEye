# Importing Libraries
import RPi.GPIO as GPIO
import PCF8591 as ADC   # Not needed yet, but I think I do....
import smbus
import time

import Adafruit_DHT

# Referencing the other py files
from StartUpSequence import *
from Diagnostic import *
from ButtonHandler import ButtonHandler
from UsingAllSensors import *
from Adafruit_BMP import BMP085
# import Adafruit_DHT

# Configures GPIO to use Broadcom chip numbering scheme.
GPIO.setmode(GPIO.BCM)

# Configuring Pins
BtnPin = 18
TempPin = 7
HumPin = 23 # or 16

# Temp Pin Setup
db18b20 = ''

# Hum Pin Setup
hum_sensor = Adafruit_DHT.DHT22 # Can change to DHT11

# Bar Pin Setup
bus = smbus.SMBus(1)
barometer_sensor = BMP085.BMP085(busnum=1)


# Sets up the sensors.
def setup():
  GPIO.setup(BtnPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
  GPIO.setup(TempPin, GPIO.IN)
  GPIO.setup(HumPin, GPIO.IN)

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
  
  diagnostic_check(BtnPin, TempPin, HumPin, hum_sensor, barometer_sensor)


if __name__ == "__main__":
  # GPIO.cleanup() -- Not needed atm, but kept

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
    #button_handler.cleanup()
    GPIO.cleanup()
