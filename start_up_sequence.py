# Start up sequence to run every time it turns on.
# Checking for sensor communication.



# Referencing other py files
from diagnostic_check import diagnostic_check()

def start_up_sequence():
    print("Starging up...")

    if not diagnostic_check():
        return False
    return True
