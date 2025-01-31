# Importing Libraries
import RPi.GPIO as GPIO
import time
import os
import sys
from datetime import datetime

# Importing Modules
import LED
import collect_data
import database
import diagnostic

class ModeSelection:
    def __init__(self, conn, barometer_sensor, camera, D_BTN, M_BTN, TEMP_PIN, HUM_PIN):
        self.conn = conn
        self.barometer_sensor = barometer_sensor
        self.camera = camera
        self.D_BTN = D_BTN
        self.M_BTN = M_BTN
        self.TEMP_PIN = TEMP_PIN
        self.HUM_PIN = HUM_PIN

    def mode_select(self):
        press_start = None
        mode_selected = False

        while True:
            if GPIO.input(self.D_BTN) == GPIO.LOW:
                press_start = time.time()
                while GPIO.input(self.D_BTN) == GPIO.LOW:
                    press_duration = time.time() - press_start

                    if press_duration >= 3 and not mode_selected:
                        print("Long hold detected: Drone Mode")
                        LED.stop()
                        mode_select = True
                        return 'drone'
                    
                if not mode_selected:
                    print("Short press detected: Walk Mode")
                    LED.stop()
                    return 'walk'
                
            if GPIO.input(self.M_BTN) == GPIO.LOW:
                print("Second button press")
                press_start = time.time()
                while GPIO.input(self.M_BTN) == GPIO.LOW:
                    pass

                press_duration = time.time() - press_start

                if press_duration >= 1:
                    print("Long hold detected: Reboot")
                    LED.solid('red')
                    GPIO.cleanup()
                    sys.exit() # REPLACE WITH REBOOT WHEN FINALIZED
                else:
                    print("Short press detected: Diagnostics initialized")
                    diagnostic.diagnostic_check(self.D_BTN, self.M_BTN, self.TEMP_PIN, self.HUM_PIN, self.barometer_sensor, self.camera)
                    LED.stop()
            
            LED.solid('white')
            time.sleep(0.1)

    
    
    """
    For now, Drone Mode collects only a certain number of times.

    The idea is that once a GPS is added, it would collect everything until
    a. Initial GPS location is reached
    b. **NEEDS TO BE IMPLEMENTED** A stop button has been pressed


    I'm thinking when it's in drone mode, it's pulsing green, make it so if the M_BTN is short pressed
    it would stop collecting data (it would still to the complete_flight sequence)
    
    """
    
    def drone_mode(self):
        print("DRONE MODE")
        LED.stop()
        LED.pulse('green')

        DATA_ALTITUDE_THRESHOLD = 10
        starting_alt = collect_data.read_alt(self.baromter_sensor)

        while True:
            time.sleep(2)
            current_alt = collect_data.read_alt(self.baromter_sensor)
            altitude_diff = abs(current_alt - starting_alt)

            print(f"Current Altitude: {current_alt} ft. | Difference: {round(altitude_diff, 3)} ft.")

            if altitude_diff >= DATA_ALTITUDE_THRESHOLD:
                print(f"Altitude threshold reached: {altitude_diff} ft. Starting data collection.")
                break

            flight_start_time = datetime.now()
            flight_id = database.collect_flight_data(self.conn, self.barometer_sensor, self.camera, interval=20, i=0)

            for i in range(1, 3):
                database.collect_flight_data(self.conn, self.barometer_sensor, self.camera, interval=20, i=0)

            flight_end_time = datetime.now()
            database.complete_flight(self.conn, flight_id, flight_end_time)

            LED.stop()
            print("Flight data collection complete!")

    def walk_btn(self):
        while GPIO.input(self.M_BTN) == GPIO.HIGH:
            pass

        press_start = time.time()
        while GPIO.input(self.M_BTN) == GPIO.LOW:
            pass
        
        press_duration = time.time() - press_start

        if 0 < press_duration < 0.5: # Changed the timing to be shorter
            print("short press, collecting data.")
            return 'short'
        elif press_duration > 1:
            print("long press, returning to mode selection.")
            return 'long'
        
        return None
    
    def walk_mode(self):
        print("WALK MODE")

        while True:
            LED.stop()
            LED.solid('green')

            press_type = self.walk_btn()
            if press_type == 'short':
                print("Collecting Data.")
                database.collect_walk_data(self.conn, self.baromter_sensor, self.camera)
            elif press_type == 'long':
                print("Exit Walk Mode")
                LED.stop()
                return
            else:
                print("invalid")
