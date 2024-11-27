'''
Diagostic.py is a diagnostic check meant to run in start_up and any
time the button is pressed.

ADD THE LIGHT AND SCREEN LOGIC


So it knows when it's powered on/off, but not if it's capable to 
output some signal
'''
# Importing Libraries
import RPi.GPIO as GPIO
import os

BtnPin = 12
TempPin = 11
HumidityPin = 13

ds18b20 = ''
sensor_prefix = '28-'

# Accept ALL GPIO pins as parameters
def diagnostic_check(BtnPin, TempPin, HumidityPin):
    print("initializing diagnostics...")

    #GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.setup(TempPin, GPIO.IN)
    #GPIO.setup(HumidityPin, GPIO.IN)
    
    try:
        if GPIO.input(BtnPin) == 0:
            print("Diagnostic failed: Button not responding.")
            return False
        if GPIO.input(TempPin) == 0:
            print("Diagnostic failed: Temp Sensor not responding.")
            return False
        if GPIO.input(HumidityPin) == 0:
            print("Diagnostic failed: Humidity Sensor not responding.")
            return False
        for i in os.listdir('/sys/bus/w1/devices'):
            if i.startswith(sensor_prefix):
                ds18b20 = i
                break
        if not ds18b20:
            raise RuntimeError("No DS18b20 sensor dectedted!")


    except Exception as e:
        print(f"diagnostic check failed: {e}")
        return False



    print("finished diagnostic")
    return True
