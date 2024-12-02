import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
BtnPin = 18
GPIO.setup(BtnPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def callback(channel):
	print("Button pressed!")
	
GPIO.add_event_detect(BtnPin, GPIO.FALLING, callback=callback, bouncetime = 200)

try:
	print("waiting for button press...")
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	GPIO.cleanup()
finally:
	GPIO.cleanup()
