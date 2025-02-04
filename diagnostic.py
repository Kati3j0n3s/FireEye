# Import Libraries
import RPi.GPIO as GPIO
import time
import os

# Importing Modules
import error_handler
import LED
from camera_control import CameraControl
from collect_data import CollectData

# Constants
SENSOR_PREFIX = '28-' # DS18B20 Temperature Sensor Prefix

""" Initialize Diagnostic with all necessary hardware components. """
class Diagnostic:
    def __init__(self, D_BTN, M_BTN, TEMP_PIN, HUM_PIN, barometer_sensor, camera, max_retries=3, timeout=15):
         self.D_BTN = D_BTN
         self.M_BTN = M_BTN
         self.TEMP_PIN = TEMP_PIN
         self.HUM_PIN = HUM_PIN
         self.barometer_sensor = barometer_sensor
         self.camera = camera
         self.max_retries = max_retries
         self.timeout = timeout

         # Creating Instances
         self.collect_data = CollectData(barometer_sensor=self.barometer_sensor, sensor_id=self.sensor_id)
         self.camera_control = CameraControl(self)

    # Checks if Button(s) are responding
    def check_button(self, button, name):
         try:
               if time.time() - self.start_time > self.timeout:
                   error_handler.log_error(f"Diagnostic timed out during {name} check.", "check_button")
                   return False
               if GPIO.input(button) == 0:
                    error_handler.log_error(f"{name} not powered.", "check_button")
                    return False
               print(f"{name} is powered and responsive")
               return True
         
         except Exception as e:
              error_handler.log_error(str(e), "check_button")
              return False
         

    # Checks if Temperature Sensor is working
    def check_temperature_sensor(self):
         try:
               if time.time() - self.start_time > self.timeout:
                   error_handler.log_error(f"Diagnostic timed out during temperature sensor check.", "check_temperature_sensor")
                   return False
               if GPIO.input(self.TEMP_PIN) == 0:
                    error_handler.log_error("Temperature Sensor not powered.", "check_temperature_sensor")
                    return False
               
               sensor_id = self.check_ds18b20_sensor()
               if sensor_id:
                    temperature = self.collect_data.read_temp(sensor_id)
                    print(f"Temperature Sensor: Read successful, Current Temperature: {temperature}\u00b0F")
                    return True
               else:
                    error_handler.log_error("DS18B20 sensor unable to collect data.", "check_temperature_sensor")
                    return False

         except Exception as e:
              error_handler.log_error(str(e), "check_temperature_sensor")
              return False

    # Check if Humidity Sensor is working
    def check_humidity_sensor(self):
         try:
               if time.time() - self.start_time > self.timeout:
                   error_handler.log_error(f"Diagnostic timed out during humidity sensor check.", "check_humidity_sensor")
                   return False
               if GPIO.input(self.HUM_PIN_PIN) == 0:
                    error_handler.log_error("Humidity Sensor not powered.", "check_humidity_sensor")
                    return False
               
               humidity = self.collect_data.read_hum()
               if humidity:
                    print(f"Humidity Sensor: Read successful, Current Humidity: {humidity}%")
                    return True
               else:
                    error_handler.log_error("Humidity sensor unable to collect data.", "check_humidity_sensor")
                    return False

         except Exception as e:
              error_handler.log_error(str(e), "check_humidity_sensor")
              return False
         
   # Checks if Barometer Sensor is working
    def check_barometer_sensor(self):
         try:
               if time.time() - self.start_time > self.timeout:
                   error_handler.log_error(f"Diagnostic timed out during Barometer sensor check.", "check_barometer_sensor")
                   return False
               
               pressure = self.collect_data.read_pre(self.barometer_sensor)
               altitude = self.collect_data.read_alt(self.barometer_sensor)
               print(f"Barometer Sensor: Pressure = {pressure} Pa, Altitude = {altitude} meters.")
               return True
         
         except Exception as e:
              error_handler.log_error(str(e), "check_barometer_sensor")
              return False

   # Checks if Camera is working
    def check_camera(self):
         try:
               if time.time() - self.start_time > self.timeout:
                   error_handler.log_error(f"Diagnostic timed out during Camera check.", "check_camera")
                   return False
               
               if self.camera_control.test_image(self.camera):
                    print("Camera Diagnostic: Success! Camera is functiona an can take pictures.")
                    return True
               else:
                    error_handler.log_error("Camera could not capture an image.", "check_camera")
                    return False

         except Exception as e:
              error_handler.log_error(str(e), "check_camera")
              return False
         

         
   # Checks if Barometer Sensor is working
    @staticmethod
    def check_ds18b20_sensor():
         for device in os.listdir('/sys/bus/w1/devices'):
              if device.startswith(SENSOR_PREFIX):
                   return device      
         return None
    
    # Runs the full diagnostic sequence
    def run_diagnostic(self):
         LED.stop()
         LED.pulse('blue')

         retries = 0
         while retries < self.max_retries:
              self.start_time = time.time()
              print("Initializing diagnostics...")

              all_checks_passed = (
                   self.check_button(self.D_BTN, "Diagnostic Button") and
                   self.check_button(self.M_BTN, "Mode Button") and
                   self.check_temperature_sensor() and
                   self.check_humidity_sensor() and
                   self.check_barometer_sensor() and
                   self.check_camera()
              )

              if all_checks_passed:
                   print("Diagnostic check passed.")
                   LED.stop()
                   return True
              else:
                   print(f"Diagnostic check failed or timed out after {self.timeout} seconds. Retrying...")
                   retries += 1

         LED.solid('red')
         print("Diagnostic check failed after maximum retries.")
         return False
         
