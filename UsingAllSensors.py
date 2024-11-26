'''
The point of this file is just to test and mess with all the sensors
that would be used in FireEye. Also a reference file.
'''

# Importing Libraries
import RPi.GPIO as GPIO
#import PCF8591 as ADC
import time
import os

# Configures GPIO to use Broadcom chip numbering scheme.
GPIO.setmode(GPIO.BCM)
BtnPin = 12
TempPin = 7
HumidityPin = 16
#BarPin = 

# Global Variable Initialization
ds18b20 = ''

def setup():
	GPIO.setup(BtnPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(TempPin, GPIO.IN)
	GPIO.setup(HumidityPin, GPIO.IN)
	# Setting up the DS28b20 Temperature Sensor
	global ds18b20
	sensor_prefix = '28-'
	for i in os.listdir('/sys/bus/w1/devices'):
		if i.startswith(sensor_prefix):
			ds18b20 = i
			break
			
	if not ds18b20:
		raise RuntimeError("No DS18b20 sensor dectedted!")

			
def read():
	
	# Reads and returns the temp from the sensor
	try:
		location = f'/sys/bus/w1/devices/{ds18b20}/w1_slave'
		with open(location, 'r') as tfile:
			text = tfile.read()
		secondline = text.split("\n")[1]
		temperaturedata = secondline.split(" ")[9]
		temperature_celsius = float(temperaturedata[2:])/1000
		temperature_fahrenheit = (temperature_celsius * 9/5) + 32
		return temperature_fahrenheit
	except Exception as e:
		print(f"Error reading sensor: {e}")
		return None
		
		
def loop():
	while True:
		temperature = read()
		if temperature is not None:
			print(f"Current temperature: {temperature:.3f} F")
		else:
			print("Failed to read temperature.")
		time.sleep(1)
		
def data():
	setup()
	loop()
		
if __name__ == '__main__':
	try:
		setup()
		loop()
	except KeyboardInterrupt:
		print("\nExiting")
