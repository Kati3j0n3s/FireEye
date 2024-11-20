'''
StartUpSequenc.py houses the start up logic. It either ends with the
Rasbperry pi waiting for altitude change, or with Fail and will not
allow flight.

Checks for:
- Connection to Sensors
- Enough battery life, which is a function call


NOTE
This logic is placed in Main.py for now and will be moved here.
'''


# Referencing other py files
from Diagnostic import *

# def start_up_sequence(BtnPin, TempPin, HumidityPin):
#     print("Starging up...")

#     diagnostic_passed = diagnostic_check(BtnPin, TempPin, HumidityPin)

#     if not diagnostic_passed:
#         print("Startup failed: Initial diagnostic check did not pass.")
#         return False

#     print("Startup successful.")
#     return True
