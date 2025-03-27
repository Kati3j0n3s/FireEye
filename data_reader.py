"""
Data Reader

Provides functions to collect and return sensor data from connected components.
"""
from imports import *
from component_manager import ComponentManager
import config
from utils import log_error

class DataReader:
    def __init__(self, component_manager):
        """Initialize with a reference to the component manager"""
        self.components = component_manager
        self.image_path = config.IMAGE_FOLDER_PATH
        self.gps = config.gps

        # Initializing Camera Settings
        try:
            self.camera.set(cv.CAP_PROP_EXPOSURE, config.EXPOSURE)
            self.camera.set(cv.CAP_PROP_GAIN, config.GAIN)
            self.camera.set(cv.CAP_PROP_FPS, config.FPS)
            self.camera.set(cv.CAP_PROP_BRIGHTNESS, config.BRIGHTNESS)
            self.camera.set(cv.CAP_PROP_CONTRAST, config.CONTRAST)
        except Exception as e:
            log_error(e)

    """DS19B20 Temperature Sensor (Sunfounder)"""
    def read_temperature(self):
        try:
            location = self.components.ds18b20_sensor_path

            with open(location, 'r') as tfile:
                text = tfile.read()

            secondline = text.split("\n")[1]
            temperaturedata = secondline.split(" ")[9]
            temperature = float(temperaturedata[2:])
            temperature = temperature / 1000
            return temperature
        except Exception as e:
            log_error(e)
            return None
    
    """BMP085 Barometer Sensor (Sunfounder)"""
    def read_pressure(self):
        try:
            pressure = self.components.bar_sensor.read_pressure()
            return pressure
        except Exception as e:
            log_error(e)

    def read_altitude(self):
        try:
            altitude = self.components.bar_sensor.read_altitude()
            return altitude
        except Exception as e:
            log_error(e)

    def read_bmp_temperature(self):
        try:
            temperature = self.components.bar_sensor.read_temperature()
            return temperature
        except Exception as e:
            log_error(e)

    """DHT11 Humiture Sensor (Sunfounder)"""
    def read_humidity(self, humidity):
        try:
            print(f"Humidity From DHT11: {humidity}")
            return humidity
        except Exception as e:
            log_error(e)
            return None

    def read_dht11_temperature(self, temperature):
        try:
            print(f"Temperature From DHT11: {temperature}")
            return temperature
        except Exception as e:
            log_error(e)
            return None

    def read_dht11_data(self):
        try:
            result = self.get_dht11_data()
            if result:
                humidity, temperature = result
                self.read_dht11_temperature(temperature)
                self.read_humidity(humidity)
        except Exception as e:
            log_error(e)
            return None
        
    def get_dht11_data(self):
        """Reads raw data from DHT11 sensor and processes it"""
        # Source: Sunfounder Code
        MAX_UNCHANGE_COUNT = 100
        STATE_INIT_PULL_DOWN = 1
        STATE_INIT_PULL_UP = 2
        STATE_DATA_FIRST_PULL_DOWN = 3
        STATE_DATA_PULL_UP = 4
        STATE_DATA_PULL_DOWN = 5

        unchanged_count = 0
        last = -1
        data = []

        while True:
            current = GPIO.input(self.components.hum_pin)
            data.append(current)
            if last != current:
                unchanged_count = 0
                last = current
            else:
                unchanged_count += 1
                if unchanged_count > MAX_UNCHANGE_COUNT:
                    break
    
        state = STATE_INIT_PULL_DOWN
        lengths = []
        current_length = 0

        for current in data:
            current_length += 1
            if state == STATE_INIT_PULL_DOWN and current == GPIO.LOW:
                state = STATE_INIT_PULL_UP
            elif state == STATE_INIT_PULL_UP and current == GPIO.HIGH:
                state = STATE_DATA_FIRST_PULL_DOWN
            elif state == STATE_DATA_FIRST_PULL_DOWN and current == GPIO.LOW:
                state = STATE_DATA_PULL_UP
            elif state == STATE_DATA_PULL_UP and current == GPIO.HIGH:
                current_length = 0
                state = STATE_DATA_PULL_DOWN
            elif state == STATE_DATA_PULL_DOWN and current == GPIO.LOW:
                lengths.append(current_length)
                state = STATE_DATA_PULL_UP

        if len(lengths) != 40:
            return False
        
        shortest_pull_up = min(lengths)
        longest_pull_up = max(lengths)
        halfway = (longest_pull_up + shortest_pull_up) / 2
        bits = []

        for length in lengths:
            bit = 1 if length > halfway else 0
            bits.append(bit)

        the_bytes = []
        byte = 0
        for i in range(0, len(bits)):
            byte = byte << 1
            if bits[i]:
                byte = byte | 1
            if (i + 1) % 8 == 0:
                the_bytes.append(byte)
                byte = 0

        checksum = (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 0xFF
        if the_bytes[4] != checksum:
            return False
        
        return the_bytes[0], the_bytes[2]
    
    """Camera Using OpenCV"""
    def capture_image(self):
        """Capture a single image from the camera"""
        try:
            ret, frame = self.components.camera.read()
            if ret:
                if not os.path.exists(self.image_path):
                    os.makedirs(self.image_path)

                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                filename = os.path.join(self.image_path, f'{timestamp}.jpg')
                cv.imwrite(filename, frame)
            else:
                return None
        except Exception as e:
            log_error(e)

    def capture_test_image(self):
        """Capture a single image from the camera"""
        try:
            ret, frame = self.components.camera.read()
            if ret:
                cv.imwrite('test_image.jpg', frame)
            else:
                return None
        except Exception as e:
            log_error(e)

    def setup_gps(self):
        print("Setting up GPS...")

        attempts = 0        
        while not self.gps.has_fix and attempts < 3:
            self.gps.update()
            print("Waiting for GPS fix...")
            time.sleep(1)
            attempts += 1

        if self.gps.has_fix:
            print("GPS fix obtained!")
            return True
        else:
            print("Failed to obtain GPS fix after 3 attempts.")
            return False    
    
    def collect_gps_data(self):
        print("Checking GPS fix before collecting coordinates...")

        # If there is no fix, then try to set it up
        if not self.gps.has_fix:
            print("No GPS fix. Attempting to set it up...")
            if not self.setup_gps():
                print("Failed to set up GPS fix. Returning error.")
                return 0, 0, 0
            
        # If there is a fix try to collect data, in under 3 attempts
        attempts = 0
        while attempts < 3:
            self.gps.update()

            if self.gps.has_fix:
                latitude = config.gps.latitude
                longitude = config.gps.longitude
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

                print(f"Collected: {latitude}, {longitude} at {timestamp}")
                return latitude, longitude, timestamp

            print("No GPS fix available. Please wait.")
            attempts += 1
            time.sleep(1)
                
        # If after 3 attempts, no fix is found, return error values
        print("Failed to obtain GPS fix after 3 attempts")
        return 0, 0,

