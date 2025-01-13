import RPi.GPIO as GPIO
import time
import Adafruit_DHT
import math

DHT_SENSOR = Adafruit_DHT.DHT11

# Gets a single temp data value
def read_temp(sensor_id):
	
    sensor_file = f'/sys/bus/w1/devices/{sensor_id}/w1_slave'
    with open(sensor_file, 'r') as f:
        lines = f.readlines()
        
    if "YES" in lines[0]:
        temp_string = lines[1].split("t=")[-1]
        celcius_temp = float(temp_string) / 1000.0
        fahrenheit_temp = celcius_temp * 9.0 / 5.0 + 32
        return round (fahrenheit_temp, 2)
    else:
        raise RuntimeError("Failed to read temperature data from DS18b20 sensor.")

# Gets a single altitude data value
def read_alt(barometer_sensor):
	try:
		altitude_meters = barometer_sensor.read_altitude()
		altitude_feet = round(altitude_meters * 3.28084, 3)
		return altitude_feet
	except Exception as e:
		raise RuntimeError(f"Failed to read altitude data: {e}")

# Gets a single pressure data value
def read_pre(barometer_sensor):
	try:
		return barometer_sensor.read_pressure()
	except Exception as e:
		raise RuntimeError(f"Failed to read pressure data: {e}")
	
	
# Calculating the CBI based on temp and humidity
# Link: https://www.n5pa.com/wxcbicalc01.php
def calculate_cbi(temp, humidity):
    """
    Calculate the CBI (Custom Burn Index) based on temperature and humidity.

    Parameters:
    temp (float): Temperature (T) in degrees.
    humidity (float): Relative Humidity (RH) in percentage.

    Returns:
    float: The calculated CBI value.
    """
    cbi = (0.0167 * (104.5 - (1.373 * humidity) + (0.54 * temp)) * 
           (124 * math.pow(10, (-0.0142 * humidity))))
    return cbi

def determine_danger_class(CBI):
    """
    Determine the Danger Class based on the CBI value.

    Parameters:
    cbi (float): The calculated CBI value.

    Returns:
    str: The danger class ('L', 'M', 'H', 'VH', or 'E').
    """
    if CBI < 50:
        return 'Low (L)'
    elif 50 <= CBI < 75:
        return 'Moderate (M)'
    elif 75 <= CBI < 90:
        return 'High (H)'
    elif 90 <= CBI < 97.5:
        return 'Very High (VH)'
    else:
        return 'Extreme (E)'

