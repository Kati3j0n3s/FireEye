# Importing Libraries
import RPi.GPIO as GPIO
import time

# Referencing the other py files
from start_up_sequence import start_up_sequence()
from diagnostic_check import diagnostic_check()

# Establishing sensor pins
GPIO.setmode(GPIO.BOARD) # Means physical pin numbering
BtnPin = 12
TempPin = 11
HumidityPin = 13


def main():
  start_up_status = start_up_sequence()
    


if __name__ == "__main__":
  main()
