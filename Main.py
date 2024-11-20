'''
Before I go any further, I'm going to create some sort of diagram to help me out in coding. 
I already feel that I need one.
'''


# Importing Libraries
import RPi.GPIO as GPIO
import PCF8591 as ADC   # Not needed yet, but I think I do....
import time

# Referencing the other py files
from StartUpSequence import *
from Diagnostic import *
from ButtonHandler import *

# Configures GPIO to use Broadcom chip numbering scheme.
GPIO.setmode(GPIO.BCM)
BtnPin = 12
TempPin = 11
HumidityPin = 13

# MAKE SURE TO ADD THIS INTO THE MAIN LOOP
def setup():
  GPIO.setup(BtnPin, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Probably need to change PUD_UP
  GPIO.setup(TempPin, GPIO.IN)
  GPIO.setup(HumidityPin, GPIO.IN)

# Need to rename this, just have the 'main' loop be the python one
def main():
  # Try to start up, if it fails enters a loop to re-run diagnostics
  start_up_status = start_up_sequence(BtnPin, TempPin, HumidityPin)
  while not start_up_status:
    print("System idle due to to failed diagnostics. Wating for diagnostics to pass...")
    time.sleep(5)
    start_up_status = start_up_sequence(BtnPin, TempPin, HumidityPin)

  # As long as start_up_sequence() succeded, then look for user prompts
  print("System is now idle, ready for user commands.")



if __name__ == "__main__":

  # Button press indicates re-diagnostic (single press) or rest (long press, 10s)
  # configure_button()

  try:
    main()
    while True:
      time.sleep(1) # Keeps looping to keep program alive

  except KeyboardInterrupt:
    GPIO.cleanup()
