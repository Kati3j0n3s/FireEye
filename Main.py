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
import LED
import Mode

# Configures GPIO to use Broadcom chip numbering scheme.
GPIO.setmode(GPIO.BCM)

# Configuring Pins
Btn1 = 18
# Btn2 = 25
TempPin = 7
HumPin = 23
RPin = 5
GPin = 6
BPin = 13

# Bar Pin Setup
bus = smbus.SMBus(1)
barometer_sensor = BMP085.BMP085(busnum=1)

# Camera Setup
camera = Camera()

# Constants
COLLECTING_DATA_ALTITUDE_THRESHOLD = 4

# Sets up the sensors.
def setup():
  # GPIO Setups
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(Btn1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
  GPIO.setup(TempPin, GPIO.IN)
  GPIO.setup(HumPin, GPIO.IN)
  GPIO.setup(RPin, GPIO.OUT)
  GPIO.setup(GPin, GPIO.OUT)
  GPIO.setup(BPin, GPIO.OUT)
  



if __name__ == "__main__":
  try:
    setup()
    #diagnostic_check(Btn1, TempPin, HumPin, barometer_sensor, camera)
    
    # Database Setup
    conn = connect_db()
    create_tables(conn)
    
    # Mode selection call
    selected_mode = Mode.mode_select(Btn1)
    
    mode_functions = {
      'drone' : lambda: Mode.drone_mode(conn, barometer_sensor, camera),
      'walk' : lambda: Mode.walk_mode(Btn1, conn, barometer_sensor, camera)
    }
    
    if selected_mode in mode_functions:
      mode_functions[selected_mode]()
    else:
      print("Mode not selected")
    
    """Set Sensor Pack Mode"""
    '''
    Let's have start_up() actually contain the select mode function(s).
    But essentially, when diagnostic is done, have LED be white to 
    indicate it's waiting for mode selection. Have user select the mode.
    Single Press - Walking
    Long Press - Drone
    
    DRONE MODE SELECTED:
    Have the LED start to pulse green, indicating that it's waiting to reach
    a higher altitude
    - Since it's gonna be on a drone. I don't need to implement the
      collecting light.
    
    WALK MODE SELECTED:
    Have the LED be solid green, indicating that it's ready to take
    a collection (via press of 'mode' button)
    
    While it's collecting have it be solid yellow, indicating it is
    still collecting data
    - COMPLICATION: Need a non blurry picture, may have it take 3 to 5
      or so (and add it to the db) and have CompV determine which of 
      them isn't blurry, and use it for analysis.
    
    COMPLICATION:
    How do I cancel the mode?
    
    
    '''
    
    # Keeps looping to keep program alive
    time.sleep(1) 

  except Exception as e:
    print(f"Error: {e}")
    
  finally:
    GPIO.cleanup()
    #if conn: UNCOMMENT WHEN FIXED
      #conn.close() UNCOMMENT WHEN FIXED
