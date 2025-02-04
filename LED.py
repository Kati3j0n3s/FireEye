'''
LED.py

THIS DIDN'T GET CHANGED

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
	'red' : [RPin, 0, 0], # Red
	'green' : [0, GPin, 0], # Green
	'blue' : [0, 0, BPin], # Blue
	'white' : [RPin, GPin, BPin], # White
	'yellow' : [RPin, GPin, 0] # Yellow
}

from threading import Thread, Event

_stop_event = Event()
thread = None
pwm_instances = []

# Pulsing function for any color
def pulse(color_name):
	global thread, pwm_instances
	_stop_event.set() # Stops ongoing threads
	_stop_event.clear() # Resets the stop event
	
	pins = colors[color_name]
	
	pwm_instances = []
	for pin in pins:
		if pin != 0:
			pwm = GPIO.PWM(pin, 1000)
			pwm.start(0)
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
	global pwm_instances
	_stop_event.set()
	time.sleep(0.1)
	
	pins = colors[color_name]
	
	for pwm in pwm_instances:
		pwm.stop()
	pwm_instances = []
	
	GPIO.output(RPin, GPIO.HIGH)
	GPIO.output(GPin, GPIO.HIGH)
	GPIO.output(BPin, GPIO.HIGH)	
	
	if pins[0] != 0:
		GPIO.output(pins[0], GPIO.LOW)
	if pins[1] != 0:
		GPIO.output(pins[1], GPIO.LOW)
	if pins[2] != 0:
		GPIO.output(pins[2], GPIO.LOW)
	
def stop():
	global pwm_instances
	_stop_event.set()
	time.sleep(0.1)
	
	for pwm in pwm_instances:
		pwm.stop()
	pwm_instances.clear()
	
	GPIO.output(RPin, GPIO.HIGH)
	GPIO.output(GPin, GPIO.HIGH)
	GPIO.output(BPin, GPIO.HIGH)


