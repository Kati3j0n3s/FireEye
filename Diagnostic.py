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
import ReadData


BtnPin = 12
TempPin = 7
HumPin = 23

# Temp sensor setup
ds18b20 = ''
sensor_prefix = '28-'


# Accept ALL GPIO pins as parameters
def diagnostic_check(BtnPin, TempPin, HumPin, barometer_sensor):
    print("initializing diagnostics...")
    
    try:
        # Diagnosing Button
        if GPIO.input(BtnPin) == 0:
            print("Diagnostic failed: Button not responding (no power).")
            return False
        else:
            print("Button is powered and responsive")
            
        # Diagnosing Temperature Sensor
        if GPIO.input(TempPin) == 0:
            print("Diagnostic failed: Temp Sensor not powered.")
        else:
            try:
                ds18b20 = check_ds18b20_sensor()
                if ds18b20:
                    temperature = ReadData.read_temp(ds18b20)
                    print(f"Temperature Sensor (DS18b20): Read successful, Current Temperature: {temperature}\u00b0F")
                else:
                    print(f"Diagnostic failed: DS18b20 sensor unable to read data.")
                
            except Exception as e:
                print(f"Diagnostic failed: Temperature Sensor (DS18b20) error. Error: {e}")
                
        # Diagnosing Humidity Sensor
        if GPIO.input(HumPin) == 0:
            print("Diagnostic failed: Humidity Sensor not powered.")
        else:
            try:
                humidity = ReadData.read_hum(HumPin)
                if humidity is not None:
                    print(f"Humidity Sensor: Read successful, Current Humidity = {humidity}%.")
                else:
                    print("Diagnostic failed: Humidity sensor unable to read data.")
            except Exception as e:
                print(f"Diagnostic failed: Humidity Sensor unable to read data. Error {e}")
                
        # Diagnosing Barometer Sensor
        try:
            pressure = ReadData.read_pre(barometer_sensor)
            altitude = ReadData.read_alt(barometer_sensor)
            print(f"Barometer Sensor: Powered and producing data, Pressure = {pressure} Pa.")
            print(f"Barometer Sensor: Powered and producing data, Altitude = {altitude} meters.")
        except Exception as e:
            print(f"Diagnostic failed: Barometer Sensor unable to read data. Error {e}")


    except Exception as e:
        print(f"Diagnostic check failed: {e}")
        return False

    print("finished diagnostic")
    return True
    
def check_ds18b20_sensor():
    for i in os.listdir('/sys/bus/w1/devices'):
        if i.startswith(sensor_prefix):
            return i
    return None
