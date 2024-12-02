import RPi.GPIO as GPIO
import time

from Humiture import *

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
		return barometer_sensor.read_altitude()
	except Exception as e:
		raise RuntimeError(f"Failed to read altitude data: {e}")

# Gets a single pressure data value
def read_pre(barometer_sensor):
	try:
		return barometer_sensor.read_pressure()
	except Exception as e:
		raise RuntimeError(f"Failed to read pressure data: {e}")

# Gets a single humidity data value
def read_hum():
	result = read_dht11_dat()
	if not result:
		return None
	else:
		humidity, temperature = result
		print(f"{humidity}")
		return humidity
	

	
