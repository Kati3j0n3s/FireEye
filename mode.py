# Importing Libraries
import RPi.GPIO as GPIO
import time
import os
import sys
from datetime import datetime

# Importing Modules
from LED import LEDController
from collect_data import CollectData
from database import FireEyeDatabase
from diagnostic import Diagnostic

class ModeSelection:
    def __init__(self, conn, barometer_sensor, camera, D_BTN, M_BTN, TEMP_PIN, HUM_PIN):
        self.conn = conn
        self.barometer_sensor = barometer_sensor
        self.camera = camera
        self.D_BTN = D_BTN
        self.M_BTN = M_BTN
        self.TEMP_PIN = TEMP_PIN
        self.HUM_PIN = HUM_PIN

        # Creating instance of collect_data, camera_control
        self.collect_data = CollectData(barometer_sensor=self.barometer_sensor, sensor_id=self.sensor_id)
        self.diagnostic = Diagnostic(self.D_BTN, self.M_BTN, self.TEMP_PIN, self.HUM_PIN, self.barometer_sensor, self.camera)
        #self.database = FireEyeDatabase(self)

    """
    Mode Select & Diagnostic/Reboot Function
    - D_BTN indidates the button for diagnostics/reboot
    - M_BTN indicates the button for mode selection (Drone/Walk)
    """
    def mode_select(self):
        press_start = None
        mode_selected = False

        while True:
            if GPIO.input(self.M_BTN) == GPIO.LOW:
                press_start = time.time()
                while GPIO.input(self.M_BTN) == GPIO.LOW:
                    press_duration = time.time() - press_start

                    if press_duration >= 3 and not mode_selected:
                        print("Long hold detected: Drone Mode")
                        self.led.stop()
                        mode_selected = True
                        return 'drone'
                    
                if not mode_selected:
                    print("Short press detected: Walk Mode")
                    self.led.stop()
                    return 'walk'
                
            if GPIO.input(self.D_BTN) == GPIO.LOW:
                print("Second button press")
                press_start = time.time()
                while GPIO.input(self.D_BTN) == GPIO.LOW:
                    pass

                press_duration = time.time() - press_start

                if press_duration >= 1:
                    print("Long hold detected: Reboot")
                    self.led.solid('red')
                    GPIO.cleanup()
                    sys.exit() # REPLACE WITH REBOOT WHEN FINALIZED
                else:
                    print("Short press detected: Diagnostics initialized")
                    self.diagnostic.diagnostic_check(self.D_BTN, self.M_BTN, self.TEMP_PIN, self.HUM_PIN, self.barometer_sensor, self.camera)
                    self.led.stop()
            
            self.led.solid('white')
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
        self.led.stop()
        self.led.pulse('green')

        DATA_ALTITUDE_THRESHOLD = 10
        starting_alt = self.collect_data.read_alt(self.baromter_sensor)

        while True:
            time.sleep(2)
            current_alt = self.collect_data.read_alt(self.baromter_sensor)
            altitude_diff = abs(current_alt - starting_alt)

            print(f"Current Altitude: {current_alt} ft. | Difference: {round(altitude_diff, 3)} ft.")

            if altitude_diff >= DATA_ALTITUDE_THRESHOLD:
                print(f"Altitude threshold reached: {altitude_diff} ft. Starting data collection.")
                break

            flight_id = self.database.collect_flight_data(self.conn, self.barometer_sensor, self.camera, interval=20, i=0)

            for i in range(1, 3):
                self.database.collect_flight_data(self.conn, self.barometer_sensor, self.camera, interval=20, i=0)

            self.database.complete_flight(self.conn, flight_id)

            self.led.stop()
            print("Flight data collection complete!")

    """
    Walk Mode collects data at each short press, after data collection 
    completion, until the M_BTN is long pressed.
    """
    def walk_btn(self):
        while GPIO.input(self.M_BTN) == GPIO.HIGH:
            pass

        press_start = time.time()
        while GPIO.input(self.M_BTN) == GPIO.LOW:
            pass
        
        press_duration = time.time() - press_start

        if 0 < press_duration < 0.5:
            print("short press, collecting data.")
            return 'short'
        elif press_duration > 1:
            print("long press, returning to mode selection.")
            return 'long'
        
        return None
    
    """
    When in Walk Mode, it waits for a short press of the M_BTN to collect data.
    """
    def walk_mode(self):
        print("WALK MODE")

        while True:
            self.led.stop()
            self.led.solid('green')

            press_type = self.walk_btn()
            if press_type == 'short':
                print("Collecting Data.")
                self.database.collect_walk_data(self.conn, self.baromter_sensor, self.camera)
            elif press_type == 'long':
                print("Exit Walk Mode")
                self.led.stop()
                return
            else:
                print("invalid")

"""
Maybe an addition feature is that when it's in either mode idle, it would have the capability to quickly
run run_diagnostic() if the D_BTN is pressed. Then once its finsihed, and it was successful, then return 
to the mode selected.

ALSO.....
Need to add something so if during collection, no other button can be pressed UNLESS it's the long press 
of D_BTN to reboot the system, just in case it hangs up during data collection.
"""
