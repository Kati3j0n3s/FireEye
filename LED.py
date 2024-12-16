'''
LED.py

Hold the preset color functions for different indicators as follows....

Blue (Solid) - Powering On
Blue (Pulsing) - Diagnostics Running
Red (Solid) - Error
Green (Solid) - Ready And Waitng
Yellow (Pulsing) - Collecting Data
Orange - Drone Mode
White - Walking Mode
'''
# Imports
import RPi.GPIO as GPIO
import time

# Configuring pins
RPin = 5
GPin = 6
BPin = 13

# Color Combinations
colors = {
	'red' : [LED.RPin, 0, 0], # Red
	'green' : [0, LED.GPin, 0], # Green
	'blue' : [0, 0, LED.BPin], # Blue
	'white' : [LED.RPin, LED.GPin, LED.BPin], # White
	'yellow' : [LED.RPin, LED.GPin, 0] # Yellow
}

from threading import Thread, Event

_stop_event = Event()

# Pulsing function for any color
def pulse(color_name):
	_stop_event.set() # Stops ongoing threads
	_stop_event.clear() # Resets the stop event
	
	pins = colors[color_name]
	
	pwm_instances = []
	for pin in pins:
		if pin != 0:
			GPI0.setup(pin, GPIO.OUT) # Not sure if this is needed
			pwm = GPIO.PWM(pin, 1000)
			pwm = start(0)
			pwm_instances.append(pwm)
	
	# Pulsing color
	def pulsing():
		while not _stop_event.is_set():
			# Fading on
			for dc in range(0, 101, 5):
				for pwm in pwm_instances:
					pwm.ChangeDutyCycle(dc)
				time.sleep(0.05)
				
			# Fading off
			for dc in range(100, -1, -5):
				for pwm in pwm_instances:
					pwm.ChangeDutyCycle(dc)
				time.sleep(0.05)
			
	thread = Thread(target=pulsing)
	thread.start()
	
def solid(color_name):
	_stop_event.set()
	
	pins = colors[color_name]
	
	for i, pin in enumerate(pins):
		if pin != 0:
			GPIO.output(pin, GPIO.LOW)
		else:
			GPIO.output(pin,GPIO.HIGH)
	
def stop():
	_stop_event.set()
	GPIO.output(RPin, GPIO.HIGH)
	GPIO.output(GPin, GPIO.HIGH)
	GPIO.output(BPin, GPIO.HIGH)
