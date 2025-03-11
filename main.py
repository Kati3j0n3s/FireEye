# Standard Libraries
import time
from datetime import datetime

# Thrid Party Libraries
import RPi.GPIO as GPIO
import smbus
from picamzero import *

# Internal Modules
from diagnostic import Diagnostic
from database import FireEyeDatabase
from mode import ModeSelection
from camera_control import CameraControl
from LED import LEDController
import error_handler

# Sensor Libraries
import BMP085

class FireEyeSystem:
    # Class Variables
    # Pin Assignments
    D_BTN = 18 #-> Btn1
    M_BTN = 25 #-> Btn2
    TEMP_PIN = 7
    HUM_PIN = 23
    R_PIN = 5
    G_PIN = 6
    B_PIN = 13

    def __init__(self):
        # GPIO Configuration
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.setup_sensors()

        # Database Instance
        self.database = FireEyeDatabase(barometer_sensor=self.barometer_sensor)

        # Setup Methods
        self.setup_camera()
        self.setup_database()
        self.setup_diagnostic()
        self.setup_modes()
        self.setup_GPIO()

        self.led = LEDController()

        # Mode Functions
        self.mode_functions = {
            'drone': lambda: self.mode.drone_mode(),
            'walk': lambda: self.mode.walk_mode()
        }

        time.sleep(0.5)

    def setup_sensors(self):
        # Barometer Sensor Setup
        try:
            self.bus = smbus.SMBus(1) # Initializes communication with I2C devices on bus 1.
            self.barometer_sensor = BMP085.BMP085(busnum=1) # Initializes the BMP085 barometer sensor for temperature and pressure measurements.
        except Exception as e:
            print("Error in setup_sensors:", e)
            error_handler.log_error(str(e), "FireEyeSystem.setup_sensors")

    def setup_camera(self):
        # Camera Setup
        try:
            self.camera = CameraControl()
        except Exception as e:
            print("Error in setup_camera:", e)
            error_handler.log_error(str(e), "FireEyeSystem.setup_camera")

    def setup_database(self):
        # Database Connection
        try:
            self.conn = self.database.connect_db()
            self.database.create_tables()
        except Exception as e:
            print("Error in setup_database:", e)
            error_handler.log_error(str(e), "FireEyeSystem.setup_database")

    def setup_diagnostic(self):
        # Diagnostic Setup
        try:
            self.diagnostic = Diagnostic(self.D_BTN, self.M_BTN, self.TEMP_PIN, self.HUM_PIN, self.barometer_sensor, self.camera)
        except Exception as e:
            print("Error in setup_diagnostic:", e)
            error_handler.log_error(str(e), "FireEyeSystem.setup_diagnostic")
    
    def setup_modes(self):
        # Mode Selection
        try:
            self.mode = ModeSelection(self.conn, self.barometer_sensor, self.camera, self.D_BTN, self.M_BTN, self.TEMP_PIN, self.HUM_PIN)
        except Exception as e:
            print("Error in setup_modes:", e)
            error_handler.log_error(str(e), "FireEyeSystem.setup_modes")

    """ Sets up GPIO and initializes database. """
    def setup_GPIO(self):
        try:
            # Sets up GPIO
            GPIO.setup(self.D_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.M_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.TEMP_PIN, GPIO.IN)
            GPIO.setup(self.HUM_PIN, GPIO.IN)
            GPIO.setup(self.R_PIN, GPIO.OUT)
            GPIO.setup(self.G_PIN, GPIO.OUT)
            GPIO.setup(self.B_PIN, GPIO.OUT)
        except Exception as e:
            error_handler.log_error(str(e), "FireEyeSystem.setup")

    """ Main loop for system operation. """
    def run(self):
        try:
            self.led.stop()
            self.led.solid('blue')
            self.diagnostic.run_diagnostic()

            while True:
                selected_mode = self.mode.mode_select()

                if selected_mode in self.mode_functions:
                    self.mode_functions[selected_mode]()
                else:
                    print("Mode not selected")
            
                time.sleep(0.5)

        except Exception as e:
            error_handler.log_error(str(e), "FireEyeSystem.run")

        finally:
            GPIO.cleanup()
            if self.conn:
                self.conn.close()

if __name__ == "__main__":
    fireeye = FireEyeSystem()
    fireeye.run()

