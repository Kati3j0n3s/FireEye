# '''
# LED.py

# THIS DIDN'T GET CHANGED

# Hold the preset color functions for different indicators as follows....

# Blue (Solid) - Powering On
# Blue (Pulsing) - Diagnostics Running
# Red (Solid) - Error
# Green (Solid) - Ready And Waitng
# Yellow (Pulsing) - Collecting Data
# Orange - Drone Mode
# White - Walking Mode
# '''
# # Imports
# import RPi.GPIO as GPIO
# import time

# # Configuring pins
# RPin = 5
# GPin = 6
# BPin = 13

# # Color Combinations
# colors = {
# 	'red' : [RPin, 0, 0], # Red
# 	'green' : [0, GPin, 0], # Green
# 	'blue' : [0, 0, BPin], # Blue
# 	'white' : [RPin, GPin, BPin], # White
# 	'yellow' : [RPin, GPin, 0] # Yellow
# }

# from threading import Thread, Event

# _stop_event = Event()
# thread = None
# pwm_instances = []

# # Pulsing function for any color
# def pulse(color_name):
# 	global thread, pwm_instances
# 	_stop_event.set() # Stops ongoing threads
# 	_stop_event.clear() # Resets the stop event
	
# 	pins = colors[color_name]
	
# 	pwm_instances = []
# 	for pin in pins:
# 		if pin != 0:
# 			pwm = GPIO.PWM(pin, 1000)
# 			pwm.start(0)
# 			pwm_instances.append(pwm)
	
# 	# Pulsing color
# 	def pulsing():
# 		while not _stop_event.is_set():
# 			# Fading on
# 			for dc in range(0, 101, 5):
# 				for pwm in pwm_instances:
# 					pwm.ChangeDutyCycle(dc)
# 				time.sleep(0.05)
				
# 			# Fading off
# 			for dc in range(100, -1, -5):
# 				for pwm in pwm_instances:
# 					pwm.ChangeDutyCycle(dc)
# 				time.sleep(0.05)
			
# 	thread = Thread(target=pulsing)
# 	thread.start()
	
# def solid(color_name):
# 	global pwm_instances
# 	_stop_event.set()
# 	time.sleep(0.1)
	
# 	pins = colors[color_name]
	
# 	for pwm in pwm_instances:
# 		pwm.stop()
# 	pwm_instances = []
	
# 	GPIO.output(RPin, GPIO.HIGH)
# 	GPIO.output(GPin, GPIO.HIGH)
# 	GPIO.output(BPin, GPIO.HIGH)	
	
# 	if pins[0] != 0:
# 		GPIO.output(pins[0], GPIO.LOW)
# 	if pins[1] != 0:
# 		GPIO.output(pins[1], GPIO.LOW)
# 	if pins[2] != 0:
# 		GPIO.output(pins[2], GPIO.LOW)
	
# def stop():
# 	global pwm_instances
# 	_stop_event.set()
# 	time.sleep(0.1)
	
# 	for pwm in pwm_instances:
# 		pwm.stop()
# 	pwm_instances.clear()
	
# 	GPIO.output(RPin, GPIO.HIGH)
# 	GPIO.output(GPin, GPIO.HIGH)
# 	GPIO.output(BPin, GPIO.HIGH)


import RPi.GPIO as GPIO
import time
from threading import Thread, Event

class LEDController:
	def __init__(self, RPin=6, GPin=6, BPin=13):
		self.RPin = RPin
		self.GPin = GPin
		self.BPin = BPin
		
		self.colors = {
				'red': [self.RPin, 0, 0],
				'green': [0, self.GPin, 0],
				'blue': [0, 0, self.BPin],
				'white': [self.RPin, self.GPin, self.BPin],
				'yellow': [self.RPin, self.GPin, 0]
		}
		
		self._stop_event = Event()
		self.thread = None
		self.pwm_instances = []

		# Setup GPIO
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.RPin, GPIO.OUT)
		GPIO.setup(self.GPin, GPIO.OUT)
		GPIO.setup(self.BPin, GPIO.OUT)

		self.stop()

	def clear_pwm(self):
		for pwm in self.pwm_instances:
			pwm.stop()
		self.pwm_instances.clear()

	def pulse(self, color_name):
		self._stop_event.set()
		self._stop_event.clear()

		self.clear_pwm()

		pins = self.colors[color_name]
		if not pins:
			raise ValueError(f"Color {color_name} not found.")
		
		self.pwm_instances = []
		for pin in pins:
			if pin != 0:
				pwm = GPIO.PWM(pin, 1000)
				pwm.start(0)
				self.pwm_instances.append(pwm)

		def pulsing():
			while not self._stop_event.is_set():
				for dc in range(0, 101, 5):
					for pwm in self.pwm_instances:
						pwm.ChangeDutyCycle(dc)
					time.sleep(0.05)
				
				for dc in range(100, -1, -5):
					for pwm in self.pwm_instances:
						pwm.ChangeDutyCycle(dc)
					time.sleep(0.05)
		
		self.thread = Thread(target=pulsing)
		self.thread.start()

	def solid(self, color_name):
		self._stop_event.set()
		time.sleep(0.1)

		self.clear_pwm()

		GPIO.output(self.RPin, GPIO.HIGH)
		GPIO.output(self.GPin, GPIO.HIGH)
		GPIO.output(self.BPin, GPIO.HIGH)

		pins = self.colors.get(color_name, None)
		if not pins:
			raise ValueError(f"Color {color_name} not found.")
		
		if pins[0] != 0:
			GPIO.output(pins[0], GPIO.LOW)
		if pins[1] != 0:
			GPIO.output(pins[1], GPIO.LOW)
		if pins[2] != 0:
			GPIO.output(pins[2], GPIO.LOW)
	
	def stop(self):
		self._stop_event.set()
		time.sleep(0.1)

		self.clear_pwm()

		GPIO.output(self.RPin, GPIO.HIGH)
		GPIO.output(self.GPin, GPIO.HIGH)
		GPIO.output(self.BPin, GPIO.HIGH)

	def cleanup(self):
		self.stop()
		GPIO.cleanup()