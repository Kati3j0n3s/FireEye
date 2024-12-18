import RPi.GPIO as GPIO
import time
import LED

def mode_select(Btn):
	# Waiting for button press
	while GPIO.input(Btn) == GPIO.HIGH:
		LED.solid('white')
		pass # Keep going till pressed
		
	# Measuring time of button press
	press_start = time.time()
	while GPIO.input(Btn) == GPIO.LOW:
		pass
	press_duration = time.time() - press_start
	
	if press_duration >= 2:
		print("Long hold detected: Drone mode")
		LED.stop()
		return 'drone'
	elif press_duration < 2:
		print("Short press detected: Walk mode")
		LED.stop()
		return 'walk'
	else:
		print("Invalid press")
		LED.stop()
		return None
		
def drone_mode():
	print("DRONE MODE")
	""" Light Indications """
	LED.stop()
	LED.pulse('green')
	
	
	
def walk_mode():
	print("WALK MODE")
	""" Light Indications """
	LED.stop()
	LED.solid('green')
	return None
	
