# Duration of LONG_PRESS in seconds
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
BtnPin = 12
LONG_PRESS = 10

def configure_button():
  GPIO.setup(BtnPin, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Set pin as input with pull-up resistor
  GPIO.add_event_detect(BtnPin, GPIO.FALLING, callback = button_callback, bouncetime = 200)

def button_callback(channel):
    start_time = time.time()
    while GPIO.input(BtnPin) == GPIO.LOW:
        time.sleep(0.1) # Debouncing?

    press_duration = time.time() - start_time

    if press_duration >= LONG_PRESS_DURATION:
        print("Long press detected. Resetting system...")
        start_up_sequence(BtnPin, TempPin, HumidityPin)
    else:
        print("Single press detected. Running diagnostic check...")
        diagnostic_check(BtnPin, TempPin, HumidityPin)


    
