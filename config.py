"""
Configuration File

Stores system-wide constants, GPIO pin mappings, and database connection settings.
"""

from imports import *

# GPIO Pin Assignments
TEMP_PIN = 7
HUM_PIN = 23
D_BTN = 18 #-> Diagnostics Button
M_BTN = 25 #-> Mode Selection Button
R_PIN = 5
G_PIN = 6
B_PIN = 13

# DS18B20 Temperature Sensor
DS18B20_SENSOR_ID = '28-031590bf4aff'
DS18B20_FILE_PATH = '/sys/bus/w1/devices/{}/w1_slave'.format(DS18B20_SENSOR_ID)

# Saved Images Path
IMAGE_FOLDER_PATH = '/home/username/FireEye/FireEye Images'

# Camera Settings
EXPOSURE = -5
GAIN = 0.4
FPS = 30
BRIGHTNESS = 0.6
CONTRAST = 0.7

# GPS
UART_PORT = "/dev'serial0"
BAUDRATE = 9600
TIMEOUT = 10
uart = serial.Serial(UART_PORT, baudrate=BAUDRATE, timeout=TIMEOUT)
gps = adafruit_gps.GPS(uart, debug=False)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0") # GGA & RMC data
gps.send_command(b"PMTK220,1000") # 1Hz update rate