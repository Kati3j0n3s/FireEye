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

# Configures GPIO to use Broadcom chip numbering scheme.
GPIO.setmode(GPIO.BCM)

# Configuring Pins
BtnPin = 18
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
  GPIO.setup(BtnPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
  GPIO.setup(TempPin, GPIO.IN)
  GPIO.setup(HumPin, GPIO.IN)
  GPIO.setup(RPin, GPIO.OUT)
  GPIO.setup(GPin, GPIO.OUT)
  GPIO.setup(BPin, GPIO.OUT)
  #GPIO.add_event_detect(BtnPin, GPIO.BOTH, callback=detect, bouncetime=200)
  

# Start up sequence
def start_up():
  diagnostic_check(BtnPin, TempPin, HumPin, barometer_sensor, camera)
  
def collecting_data(conn, barometer_sensor):
  start_data_collection(conn, barometer_sensor, camera)


if __name__ == "__main__":
  # GPIO.cleanup() -- Not needed atm, but kept

  try:
    setup()
    LED.stop()
    start_up()
    
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
    
    

    # This checks for when the sensor pack is 10ft off the starting altitude
    # LED.solid(GPin)
    # print(f"Starting altitude: {starting_alt} ft")
    
    # current_alt = starting_alt
    # while True:
      # current_alt = read_alt(barometer_sensor)
      # altitude_diff = abs(current_alt - starting_alt)
      
      # print(f"Current Altitude: {current_alt} ft. | Difference: {round(altitude_diff, 3)} ft.")
      
      # if altitude_diff >= COLLECTING_DATA_ALTITUDE_THRESHOLD:
        # print(f"Altitude threshold reached: {altitude_diff} ft. Starting data collection.")
        # break
        
      # time.sleep(0.5)
    
    
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
    #if conn: UNCOMMENT WHEN FIXED
      #conn.close() UNCOMMENT WHEN FIXED
