# Diagnostic check to be run initially and when called if
# user calls for it.
import RPi.GPIO as GPIO

BtnPin = 12
TempPin = 11
HumidityPin = 13

# Accept ALL GPIO pins as parameters
def diagnostic_check(BtnPin, TempPin, HumidityPin):
    print("initializing diagnostics...")

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(TempPin, GPIO.IN)
    GPIO.setup(HumidityPin, GPIO.IN)
    
    try:
        if GPIO.input(BtnPin) == 0:
            print("Diagnostic failed: Button not responding.")
            return False
        if GPIO.input(TempPin) == 0:
            print("Diagnostic failed: Temp Sensor not responding.")
            return False
        if GPIO.input(HumidityPin) == 0:
            print("Diagnostic failed: Humidity Sensor not responding.")
            return False


    except Exception as e:
        print(f"diagnostic check failed: {e}")
        return False



    print("finished diagnostic")
    return True
