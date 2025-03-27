# Importing Libraries
import RPi.GPIO as GPIO
import PCF8591 as ADC   # Not needed yet, but I think I do....
import smbus
import time
import sqlite3
import os
import adafruit_gps

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
Btn2 = 25
TempPin = 7
HumPin = 23
RPin = 5
GPin = 6
BPin = 13
RX = 15 # GET THE ACTUAL PIN NUMBER
TX = 14 # GET THE ACTUAL PIN NUMBER

# Bar Pin Setup
bus = smbus.SMBus(1)
barometer_sensor = BMP085.BMP085(busnum=1)

# Camera Setup
camera = Camera()

# GPS Setup
gps = None

# Constants
COLLECTING_DATA_ALTITUDE_THRESHOLD = 4

# Sets up the sensors.
def setup():
  # GPIO Setups
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  GPIO.setup(Btn1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
  GPIO.setup(Btn2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
  GPIO.setup(TempPin, GPIO.IN)
  GPIO.setup(HumPin, GPIO.IN)
  GPIO.setup(RPin, GPIO.OUT)
  GPIO.setup(GPin, GPIO.OUT)
  GPIO.setup(BPin, GPIO.OUT)

  # GPS Initialization
  global gps
  uart = busio.UART(TX, RX, baudrate=9600, timeout=10)
  gps = adafruit_gps.GPS(uart, debug=False)

  # GPS Configuration
  gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
  gps.send_command(b"PMTK220,1000")
  print("GPS Initialized")
  

if __name__ == "__main__":
  
  try:
    setup()
    LED.stop()
    diagnostic_check(Btn1, Btn2, TempPin, HumPin, barometer_sensor, camera, gps)
    
    # Database Setup
    conn = connect_db()
    create_tables(conn)
    
    while True:
      # Mode selection call
      selected_mode = Mode.mode_select(Btn1, Btn2, TempPin, HumPin, barometer_sensor, camera)
    
      mode_functions = {
        'drone' : lambda: Mode.drone_mode(conn, barometer_sensor, camera),
        'walk' : lambda: Mode.walk_mode(Btn1, conn, barometer_sensor, camera)
      }
    
      if selected_mode in mode_functions:
        mode_functions[selected_mode]()
      else:
        print("Mode not selected")
    
      # Keeps looping to keep program alive
      time.sleep(0.5) 

  except Exception as e:
    print(f"Error: {e}")
    
  finally:
    GPIO.cleanup()
    if conn:
      conn.close()
