import RPi.GPIO as GPIO
import time

# GPIO Pin Setup
red_pin = 5   # GPIO pin connected to the red pin of the LED
green_pin = 6 # GPIO pin connected to the green pin of the LED
blue_pin = 13  # GPIO pin connected to the blue pin of the LED

# GPIO Mode Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(blue_pin, GPIO.OUT)

def turn_off_led():
    GPIO.output(red_pin, GPIO.HIGH)  # Turn off red
    GPIO.output(green_pin, GPIO.HIGH)  # Turn off green
    GPIO.output(blue_pin, GPIO.HIGH)  # Turn off blue

def cleanup():
    GPIO.cleanup()

try:
    turn_off_led()  # Ensure LED starts off
    while True:
        # Example: Turn on red
        GPIO.output(red_pin, GPIO.LOW)  # Red on
        time.sleep(1)
        turn_off_led()  # Turn off all
        time.sleep(1)

except KeyboardInterrupt:
    cleanup()
