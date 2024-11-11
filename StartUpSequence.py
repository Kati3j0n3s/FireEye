# Start up sequence to run every time it turns on.
# Checking for sensor communication.



# Referencing other py files
from diagnostic_check import diagnostic_check()

def start_up_sequence(BtnPin, TempPin, HumidityPin):
    print("Starging up...")

    diagnostic_passed = diagnostic_check(BtnPin, TempPin, HumidityPin)

    if not diagnostic_passed:
        print("Startup failed: Initial diagnostic check did not pass.")
        return False

    print("Startup successful.")
    return True
