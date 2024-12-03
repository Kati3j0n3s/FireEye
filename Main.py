# Importing Libraries
import RPi.GPIO as GPIO
import PCF8591 as ADC   # Not needed yet, but I think I do....
import smbus
import time
import sqlite3

# Referencing the other py files
from Diagnostic import *
from ReadData import *
from Adafruit_BMP import BMP085
from Database import *
from datetime import datetime
from CameraData import *
from picamzero import *
from humiture import *

# Configures GPIO to use Broadcom chip numbering scheme.
GPIO.setmode(GPIO.BCM)

# Configuring Pins
BtnPin = 18
TempPin = 7
HumPin = 23

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
  diagnostic_check(BtnPin, TempPin, HumPin, barometer_sensor, camera)
  
def collecting_data(conn, barometer_sensor):
  start_data_collection(conn, barometer_sensor, camera)


if __name__ == "__main__":
  # GPIO.cleanup() -- Not needed atm, but kept

  try:
    # Sets up the necessary pins
    setup()
    
    # Runs initial diagnostic
    start_up()
    
    
    
    # Starts collecting data and adding to database
    conn = connect_db()
    create_tables(conn)
    collecting_data(conn, barometer_sensor)
    
    # Keeps looping to keep program alive
    time.sleep(1) 

  except Exception as e:
    print(f"Error: {e}")
    
  finally:
    GPIO.cleanup()
    if conn: 
      conn.close()
