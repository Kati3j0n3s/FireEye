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

led_on = False

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
	
	light_value = ADC.read(0)
	print(f"Initial Light Level: {light_value}")
	# if light_value > LIGHT_THRESHOLD:
		# set_led_state(True)
	# else:
		# set_led_state(False)
		
	set_led_state(False)
		
	time.sleep(1) # Maybe fore IR sensor initialization setup time?
	
# Sets the RGB to specific state of either ON or OFFs
def set_led_state(state):
	global led_on
	led_on = state
	GPIO.output(Rpin, GPIO.LOW if state else GPIO.HIGH)
	GPIO.output(Gpin, GPIO.LOW if state else GPIO.HIGH)
	GPIO.output(Bpin, GPIO.LOW if state else GPIO.HIGH)
	print(f"LED State Set TO: {'OFF' if state else 'ON'}")
	
	
def touch_control():
	global led_on
	if GPIO.input(TouchPin) == GPIO.HIGH:
		led_on = not led_on
		set_led_state(led_on)
		print(f"Touch Detected! LED State: {'ON' if led_on else 'OFF'}")
		time.sleep(0.3)
		
def motion_and_light_control():
	global led_on
	light_value = ADC.read(0)
	print(f"Light Level: {light_value}")
	
	ir_state = GPIO.input(IR)
	print(f"IR Motion Sensor State: {'Motion Detected' if ir_state == GPIO.LOW else 'No Motion Detected'}")
	
	if light_value > LIGHT_THRESHOLD and ir_state == GPIO.LOW and not led_on:
		print("MOTION DETECTED")
		set_led_state(True)
		time.sleep(30)
		set_led_state(False)
	else:
		print("Conditions not met for turning on LEDs")

	

def loop():
	while True:
		touch_control()
		print("Checking motion and light conditions...")
		motion_and_light_control()
		time.sleep(0.1) # Not sure if this is necessary, may need to remove


if __name__ == "__main__":
	try:
		setup()
		loop()
	except KeyboardInterrupt:
		GPIO.cleanup()
		print("Program terminated")
