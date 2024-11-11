# Importing Libraries
import RPi.GPIO as GPIO
import time

# Referencing the other py files
from start_up_sequence import start_up_sequence()
from diagnostic_check import diagnostic_check()
from ButtonHandler import *

# Establishing sensor pins via physical pin numbering
GPIO.setmode(GPIO.BOARD)
BtnPin = 12
TempPin = 11
HumidityPin = 13


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
  configure_button()

  try:
    main()
    while True:
      time.sleep(1) # Keeps looping to keep program alive

  except KeyboardInterrupt:
    GPIO.cleanup()
