import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
pin = 12
GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def callback(channel):
	print("Button pressed!")
	
GPIO.add_event_detect(pin, GPIO.FALLING, callback=callback, bouncetime = 200)

try:
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	GPIO.cleanup()
