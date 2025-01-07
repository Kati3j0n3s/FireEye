'''
Diagostic.py is a diagnostic check meant to run in start_up and any
time the button is pressed.
'''
# Importing Libraries
import RPi.GPIO as GPIO
import os
import time

from ReadData import *
from CameraData import *
from humiture import *
import LED

# Establishing Pins
Btn1 = 12
Btn2 = 25
TempPin = 7
HumPin = 24

# Humidity Constants
MAX_UNCHANGE_COUNT = 100

STATE_INIT_PULL_DOWN = 1
STATE_INIT_PULL_UP = 2
STATE_DATA_FIRST_PULL_DOWN = 3
STATE_DATA_PULL_UP = 4
STATE_DATA_PULL_DOWN = 5

# Temp sensor setup
ds18b20 = ''
sensor_prefix = '28-'


# Accept ALL GPIO pins as parameters
def diagnostic_check(Btn1, Btn2, TempPin, HumPin, barometer_sensor, camera):
    # Color Indicator
    LED.pulse('blue')
    
    print("initializing diagnostics...")
    
    # tracking if any error occurs
    diagnostic_failed = False
    
    try:
        # Diagnosing Button 1
        if GPIO.input(Btn1) == 0:
            print("Diagnostic failed: Button not responding (no power).")
            diagnostic_failed = True
        else:
            print("Button 1 is powered and responsive")
            
        # Diagnosing Button 2
        if GPIO.input(Btn2) == 0:
            print("Diagnostic failed: Button not responding (no power).")
            diagnostic_failed = True
        else:
            print("Button 2 is powered and responsive")
            
        # Diagnosing Temperature Sensor
        if GPIO.input(TempPin) == 0:
            print("Diagnostic failed: Temp Sensor not powered.")
            diagnostic_failed = True
        else:
            try:
                ds18b20 = check_ds18b20_sensor()
                if ds18b20:
                    temperature = read_temp(ds18b20)
                    print(f"Temperature Sensor (DS18b20): Read successful, Current Temperature: {temperature}\u00b0F")
                else:
                    print(f"Diagnostic failed: DS18b20 sensor unable to read data.")
                    diagnostic_failed = True
                
            except Exception as e:
                print(f"Diagnostic failed: Temperature Sensor (DS18b20) error. Error: {e}")
                diagnostic_failed = True
                
        # Diagnosing Humidity Sensor
        if GPIO.input(HumPin) == 0:
            print("Diagnostic failed: Humidity Sensor not powered.")
            diagnostic_failed = True
        else:
            try:
                humidity = hum_main()
                if humidity:
                    print(f"Humidity Sensor: Read successful, Current Humidity = {humidity}%.")
                else:
                    print("Diagnostic failed: Humidity sensor unable to read data.")
                    diagnostic_failed = True
            except Exception as e:
                print(f"Diagnostic failed: Humidity Sensor unable to read data. Error {e}")
                diagnostic_failed = True
                
        # Diagnosing Barometer Sensor
        try:
            pressure = read_pre(barometer_sensor)
            altitude = read_alt(barometer_sensor)
            print(f"Barometer Sensor: Powered and producing data, Pressure = {pressure} Pa.")
            print(f"Barometer Sensor: Powered and producing data, Altitude = {altitude} meters.")
        except Exception as e:
            print(f"Diagnostic failed: Barometer Sensor unable to read data. Error {e}")
            diagnostic_failed = True
            
        # Diagnosing Camera
        try:
            if test_image(camera):
                print("Camera diagnostic: Success! Camera is functional and can take pictures.")
            else:
                print("Diagnostic failed: Camera could not capture an image.")
                diagnostic_failed = True
        except Exception as e:
            print(f"Diagnostic failed: Camera error. Error: {e}")
            diagnostic_failed = True

    except Exception as e:
        LED.solid('red')
        print(f"Diagnostic check failed: {e}")
        diagnostic_failed = True
        
    # After Diagnostics
    if diagnostic_failed:
        # Keep red till button press
        LED.solid('red')
    else:
        print("finished diagnostic")
        LED.stop()
        return True
    
def check_ds18b20_sensor():
    for i in os.listdir('/sys/bus/w1/devices'):
        if i.startswith(sensor_prefix):
            return i
    return None

