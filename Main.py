# Importing Libraries
import RPi.GPIO as GPIO
import PCF8591 as ADC   # Not needed yet, but I think I do....
import smbus
import time
import sqlite3

# Referencing the other py files
from StartUpSequence import *
from Diagnostic import *
#from ButtonHandler import ButtonHandler
from UsingAllSensors import *
from ReadData import *
from Adafruit_BMP import BMP085
from Database import *
from datetime import datetime
from CameraData import *
from picamzero import *

# Configures GPIO to use Broadcom chip numbering scheme.
GPIO.setmode(GPIO.BCM)

# Configuring Pins
BtnPin = 18
TempPin = 7
HumPin = 23 # or 16

# Temp Pin Setup
db18b20 = ''

# Bar Pin Setup
bus = smbus.SMBus(1)
barometer_sensor = BMP085.BMP085(busnum=1)

# Camera Setup
camera = Camera()

# Sets up the sensors.
def setup():
  GPIO.setup(BtnPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
  GPIO.setup(TempPin, GPIO.IN)
  GPIO.setup(HumPin, GPIO.IN)
  #camera.start_preview()

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
  
  diagnostic_check(BtnPin, TempPin, HumPin, barometer_sensor, camera)
  
def collecting_data(conn, barometer_sensor):
  start_data_collection(conn, barometer_sensor, camera)



if __name__ == "__main__":
  # GPIO.cleanup() -- Not needed atm, but kept

  try:
    setup()
    start_up()
    # For now, cause it's dumb, giving up on button implementation
    # button_handler = ButtonHandler(pin = BtnPin, LONG_PRESS = 10)
    
    conn = connect_db()
    create_tables(conn)
    collecting_data(conn, barometer_sensor)
    
    time.sleep(1) # Keeps looping to keep program alive

  except Exception as e:
    print(f"Error: {e}")
    
  finally:
    GPIO.cleanup()
    if conn: 
      conn.close()
