"""
Component Manager

Handles GPIO initialization and sets up all hardware components (sensors, buttons, etc.).
"""

from imports import *
import config
from utils import log_error

class ComponentManager:
    def __init__(self):
        """Initialize All Hardware Components"""
        try:
            GPIO.setmode(GPIO.BCM)

            # Initialize Sensors
            self.temp_pin = config.TEMP_PIN
            self.hum_pin = config.HUM_PIN
            self.bar_sensor = BMP085.BMP085()
            self.ds18b20_sensor_path = config.DS18B20_FILE_PATH

            # Initialize Control Components
            self.r_pin = config.R_PIN
            self.g_pin = config.G_PIN
            self.b_pin = config.B_PIN
            self.d_button = config.D_BTN
            self.m_button = config.M_BTN

            # Set Pin Modes
            GPIO.setup(self.temp_pin, GPIO.IN)
            GPIO.setup(self.hum_pin, GPIO.OUT)
            GPIO.setup(self.r_pin, GPIO.OUT)
            GPIO.setup(self.g_pin, GPIO.OUT)
            GPIO.setup(self.b_pin, GPIO.OUT)
            GPIO.setup(self.d_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.d_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            # Initialize Camera for OpenCV
            self.camera = cv.VideoCapture(0)
            if not self.camera.isOpened():
                log_error("Error: Camera could not be initialized.")
        
        except Exception as e:
            log_error(e)



    def cleanup(self):
        """Releases GPIO resources when shutting down"""
        GPIO.cleanup()
        if self.camera.isOpened():
            self.camera.release()
