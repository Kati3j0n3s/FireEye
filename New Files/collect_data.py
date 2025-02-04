# Import Libraries
import RPi.GPIO as GPIO
import time
import math

# Import Modules
import error_handler

class CollectData:
    HUM_PIN = 24

    def __init__(self, barometer_sensor, temperature_sensor_id):
        self.barometer_sensor = barometer_sensor
        self.temperature_sensor_id = temperature_sensor_id
        # GPIO.setmode(GPIO.BCM) - Why needed? Already established?

    """ Gets single temperature data value. """
    def read_temp(self):
        sensor_file = f'/sys/bus/w1/devices/{self.temperature_sensor_id}/w1_slave'
        try:
            with open(sensor_file, 'r') as f:
                lines = f.readlines()

            if "YES" in lines[0]:
                temp_string = lines[1].split("t=")[-1]
                celcius_temp = float(temp_string) / 1000.0
                fahrenheit_temp = celcius_temp * 9.0 / 5.0 + 32
                return round(fahrenheit_temp, 2)
            else:
                raise RuntimeError("Failed to read temperature data from DS18B20 sensor.")
        except Exception as e:
            error_handler.log_error(f"Error reading temperature data: {e}", "read_temp")
            raise


    """ Gets single altitude data value. """    
    def read_alt(self):
        try:
            altitude_meters = self.barometer_sensor.read_alt()
            altitude_feet = round(altitude_meters * 3.28084, 3)
            return altitude_feet
        except Exception as e:
            error_handler.log_error(f"Error reading altitude data: {e}", "read_alt")
            raise RuntimeError(f"Failed to read altitude data: {e}")
        
    """ Gets single pressure data value. """
    def read_pre(self):
        try: 
            return self.barometer_sensor.read_pressure()
        except Exception as e:
            error_handler.log_error(f"Error reading pressure data: {e}", "read_pre")
            raise RuntimeError(f"Failed to read pressure data: {e}")

    """ Reads humidity from DHT11 sensor."""   
    def read_hum(self):
        try:
            GPIO.setup(self.HUM_PIN, GPIO.OUT)
            GPIO.output(self.HUM_PIN, GPIO.HIGH)
            time.sleep(0.05)
            GPIO.output(self.HUM_PIN, GPIO.LOW)
            time.sleep(0.02)
            GPIO.setup(self.HUM_PIN, GPIO.IN, GPIO.PUD_UP)

            unchanged_count = 0
            last = -1
            data = []
            MAX_UNCHANGE_COUNT = 100

            while True:
                current = GPIO.input(self.HUM_PIN)
                data.append(current)
                if last != current:
                    unchanged_count = 0
                    last = current
                else:
                    unchanged_count += 1
                    if unchanged_count > MAX_UNCHANGE_COUNT:
                        break

            if len(data) < 40:
                return None
            
            lengths = []
            current_length = 0
            for current in data:
                current_length += 1
                lengths.append(current_length)

            if len(lengths) != 40:
                return None
            
            shortest_pull_up = min(lengths)
            longest_pull_up = max(lengths)
            halfway = (longest_pull_up + shortest_pull_up) / 2
            bits = []
            the_bytes = []
            byte = 0

            for length in lengths:
                bit = 1 if length > halfway else 0
                bits.append(bit)

            for i in range(0, len(bits)):
                byte = byte << 1 | bits[i]
                if (i + 1) % 8 == 0:
                    the_bytes.append(byte)
                    byte = 0

            if len(the_bytes) < 5 or (sum(the_bytes[:4]) & 0xFF) != the_bytes[4]:
                return None
            
            return the_bytes[0] # Humidity Value
        except Exception as e:
            error_handler.log_error(f"Error reading humidity data: {e}", "read_hum")  # Log the error
            return None
    
    """Calculates the CBI (Custom Burn Index) based on temperature and humidity."""
    @staticmethod
    def calculate_cbi(temp, humidity):
        return (0.0167 * (104.5 - (1.373 * humidity) + (0.54 * temp)) * (124 * math.pow(10, (-0.0142 * humidity))))
    
    """ Determines the Danger Class based on the CBI value. """
    @staticmethod
    def determine_danger_class(cbi):
        if cbi < 50:
            return 'Low (L)'
        elif 50 <= cbi < 75:
            return 'Moderate (M)'
        elif 75 <= cbi < 90:
            return 'High (H)'
        elif 90 <= cbi < 97.5:
            return 'Very High (VH)'
        else:
            return 'Extreme (E)'