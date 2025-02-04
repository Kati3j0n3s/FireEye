# Importing Libraries
import RPi.GPIO as GPIO
import time
import smbus

# Importing Modules
from diagnostic import Diagnostic
from database import FireEyeDatabase
from mode import ModeSelection
import LED
import error_handler

#from Adafruit_BMP import BMP085
import BMP085 #testing
from picamzero import *
from datetime import datetime

class FireEyeSystem:
    def __init__(self):
        # GPIO Configuration
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Pin Assignments
        self.D_BTN = 18 #-> Btn1
        self.M_BTN = 25 #-> Btn2
        self.TEMP_PIN = 7
        self.HUM_PIN = 23
        self.R_PIN = 5
        self.G_PIN = 6
        self.B_PIN = 13

        # Barometer Sensor Setup
        self.bus = smbus.SMBus(1) # Initializes communication with I2C devices on bus 1.
        self.barometer_sensor = BMP085.BMP085(busnum=1) # Initializes the BMP085 barometer sensor for temperature and pressure measurements.

        # Camera Setup
        self.camera = Camera() 

        # Database Connection
        self.conn = None

        # Creating instance of diagnostic, database, mode_selection
        self.diagnostic = Diagnostic(self.D_BTN, self.M_BTN, self.TEMP_PIN, self.HUM_PIN, self.barometer_sensor, self.camera)
        self.database = FireEyeDatabase(self)

        # Mode Select Functions
        self.mode_functions = {
            'drone': lambda: self.mode.drone_mode(self.conn, self.barometer_sensor, self.camera),
            'walk': lambda: self.mode.walk_mode(self.D_BTN, self.conn, self.barometer_sensor, self.camera)
        }

        

    """ Sets up GPIO and initializes database. """
    def setup(self):
        # Sets up GPIO
        GPIO.setup(self.D_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.M_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.TEMP_PIN, GPIO.IN)
        GPIO.setup(self.HUM_PIN, GPIO.IN)
        GPIO.setup(self.R_PIN, GPIO.OUT)
        GPIO.setup(self.G_PIN, GPIO.OUT)
        GPIO.setup(self.B_PIN, GPIO.OUT)

        # Initializes Database
        self.conn = self.database.connect_db()
        self.database.create_tables(self.conn)

    """ Main loop for system operation. """
    def run(self):
        try:
            self.setup()
            LED.stop()
            self.diagnostic.run_diagnostic(
                self.D_BTN, self.M_BTN, self.TEMP_PIN, self.HUM_PIN, self.barometer_sensor, self.camera
            )

            while True:
                selected_mode = self.mode.mode_select(
                    self.D_BTN, self.M_BTN, self.TEMP_PIN, self.HUM_PIN, self.barometer_sensor, self.camera
                )

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

