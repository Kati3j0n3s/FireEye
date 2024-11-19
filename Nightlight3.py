import PCF8591 as ADC
import RPi.GPIO as GPIO
import time

# Pin Constants
Rpin = 17
Gpin = 27
Bpin = 22
TouchPin = 18
IR = 25

LIGHT_THRESHOLD = 150

led_on = True

def setup():
	# Board Setup Type
	GPIO.setmode(GPIO.BCM)
	
	GPIO.setup(Rpin, GPIO.OUT)
	GPIO.setup(Gpin, GPIO.OUT)
	GPIO.setup(Bpin, GPIO.OUT)
	GPIO.setup(TouchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(IR, GPIO.IN)
	
	ADC.setup(0x48)
	
	# Turn off LEDs initally
	GPIO.output(Rpin, GPIO.HIGH)
	GPIO.output(Gpin, GPIO.HIGH)
	GPIO.output(Bpin, GPIO.HIGH)
	
# Sets the RGB to specific state of either ON or OFFs
def set_led_state(state):
	global led_on
	led_on = state
	GPIO.output(Rpin, state)
	GPIO.output(Gpin, state)
	GPIO.output(Bpin, state)
	print(f"LED State Set TO: {'OFF' if state else 'ON'}")
	
	
def touch_control():
	global led_on
	if GPIO.input(TouchPin) == GPIO.HIGH:
		led_on = not led_on
		set_led_state(led_on)
		time.sleep(0.3)
		
def motion_and_light_control():
	global led_on
	light_value = ADC.read(0)
	print(f"Light Level: {light_value}")
	
	if light_value < LIGHT_THRESHOLD and GPIO.input(IR) == GPIO.LOW:
		print("MOTION DETECTED")
		set_led_state(True)
		time.sleep(30)
		set_led_state(False)
		
		
	# This code (for testing) is used to just turn on the light when it's dark
	# if light_value > LIGHT_THRESHOLD:
		# print("It's dark")
		# set_led_state(True)

	

def loop():
	while True:
		touch_control()
		if led_on == False:
			print(" ")
			motion_and_light_control()
		time.sleep(0.1) # Not sure if this is necessary, may need to remove


if __name__ == "__main__":
	try:
		setup()
		loop()
	except KeyboardInterrupt:
		GPIO.cleanup()
		print("Program terminated")
