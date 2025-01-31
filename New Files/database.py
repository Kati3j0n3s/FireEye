# Importing Libraries
import sqlite3
import time
from picamzero import PicamZero


# Importing Modules
import LED
import error_handler
from diagnostic import check_ds18b20_sensor
from collect_data import read_temp, read_alt, read_pre, read_hum
from datetime import datetime
from camera_control import take_picture


class FireEyeDatabase:
    def __init__(self, db_path="/home/username/FireEye GitHub/FireEye/fireeye_data.db"):
        self.db_path = db_path
        self.sensor_id = check_ds18b20_sensor()
        self.conn = self.connect_db()
        self.create_tables()

    def connect_db(self):
        """Establishes a connection to the FireEye Database."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute('PRAGMA journal_mode=WAL;')
            return conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            error_handler.log_error
            return None

    def create_tables(self):
        """Creates necessary tables if they do not exist."""
        try:
            cursor = self.conn.cursor()

            create_flights_query = """
            CREATE TABLE IF NOT EXISTS Flights(
                FlightID INTEGER PRIMARY KEY AUTOINCREMENT,
                FlightName TEXT,
                date DATE,
                start_time DATETIME,
                end_time DATETIME,
                duration INTEGER
            );
            """
            
            create_flight_data_query = """
            CREATE TABLE IF NOT EXISTS Flight_Data(
                DataID INTEGER PRIMARY KEY AUTOINCREMENT,
                FlightID INTEGER,
                timestamp DATETIME,
                lat REAL,
                log REAL,
                alt REAL,
                pre REAL,
                temp REAL,
                humidity REAL,
                CBI REAL,
                DangerClass TEXT,
                image_path TEXT
            );
            """

            create_walk_data_query = """
            CREATE TABLE IF NOT EXISTS Walk_Data(
                DataID INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                lat REAL,
                log REAL,
                alt REAL,
                pre REAL,
                temp REAL,
                humidity REAL,
                CBI REAL,
                DangerClass TEXT,
                image_path TEXT
            );
            """
            
            cursor.execute(create_flights_query)
            cursor.execute(create_flight_data_query)
            cursor.execute(create_walk_data_query)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def insert_flight(self, flight_name):
        """Inserts a new flight record and returns the FlightID."""
        try:
            cursor = self.conn.cursor()
            date = datetime.now().date()
            start_time = datetime.now()
            cursor.execute("INSERT INTO Flights (FlightName, date, start_time) VALUES (?, ?, ?)",
                           (flight_name, date, start_time))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error inserting flight data: {e}")
            return None

    def insert_flight_data(self, flight_id, data):
        """Inserts collected flight data."""
        try:
            cursor = self.conn.cursor()
            query = """
            INSERT INTO Flight_Data (FlightID, timestamp, lat, log, alt, pre, temp, humidity, CBI, DangerClass, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (flight_id, *data))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error inserting flight data: {e}")

    def complete_flight(self, flight_id):
        """Updates a flight with end time and duration."""
        try:
            cursor = self.conn.cursor()
            end_time = datetime.now()
            cursor.execute("SELECT start_time FROM Flights WHERE FlightID = ?", (flight_id,))
            result = cursor.fetchone()

            if not result:
                print(f"No flight found with FlightID {flight_id}")
                return

            start_time = datetime.fromisoformat(result[0])
            duration = (end_time - start_time).total_seconds()

            cursor.execute("UPDATE Flights SET end_time = ?, duration = ? WHERE FlightID = ?",
                           (end_time, duration, flight_id))
            self.conn.commit()
            print("Flight completed successfully.")
        except sqlite3.Error as e:
            print(f"Error updating flight: {e}")

    def collect_flight_data(self, barometer_sensor, camera, interval=20, i=0):
        """Simulates flight data collection and inserts it into the database."""
        try:
            flight_name = f"Flight {str(self.conn.execute('SELECT COUNT(*) FROM Flights').fetchone()[0] + 1).zfill(3)}"
            flight_id = self.insert_flight(flight_name)
            if flight_id is None:
                print("Failed to insert flight, aborting data collection.")
                return None

            timestamp = datetime.now()
            lat, log = 0.01, 0.00
            alt = read_alt(barometer_sensor)
            pre = read_pre(barometer_sensor)
            temp = read_temp(self.sensor_id)
            humidity = read_hum()
            image_name = f"image_{i}_{timestamp.strftime('%Y%m%d_%H%M%S')}.jpg"
            image_path = f"/home/username/FireEye GitHub/FireEye/FireEye Images/{image_name}"

            # Capture an image
            try:
                if take_picture(camera, image_path):
                    print(f"Image saved: {image_path}")
                else:
                    print("Failed to save image.")
            except Exception as e:
                print(f"Error capturing image: {e}")
                image_path = None

            # Calculate CBI and Danger Class
            CBI = self.calculate_cbi(temp, humidity)
            DangerClass = self.determine_danger_class(CBI)

            data = (timestamp, lat, log, alt, pre, temp, humidity, CBI, DangerClass, image_path)
            self.insert_flight_data(flight_id, data)

            print("Flight data inserted.")
            time.sleep(interval)
            return flight_id
        except Exception as e:
            print(f"Error collecting flight data: {e}")
            return None

    def collect_walk_data(self, barometer_sensor, camera):
        """Collects and inserts walk mode data."""
        try:
            LED.stop()
            LED.pulse('yellow')

            timestamp = datetime.now()
            lat, log = 0.00, 0.00
            alt = read_alt(barometer_sensor)
            pre = read_pre(barometer_sensor)
            temp = read_temp(self.sensor_id)
            humidity = read_hum()
            image_name = f"walk_image_{timestamp.strftime('%Y%m%d_%H%M%S')}.jpg"
            image_path = f"/home/username/FireEye GitHub/FireEye/FireEye Images/{image_name}"

            # Capture an image
            try:
                if take_picture(camera, image_path):
                    print(f"Image saved: {image_path}")
                else:
                    print("Failed to save image.")
            except Exception as e:
                print(f"Error capturing image: {e}")
                image_path = None

            CBI = self.calculate_cbi(temp, humidity)
            DangerClass = self.determine_danger_class(CBI)

            query = """
            INSERT INTO Walk_Data (timestamp, lat, log, alt, pre, temp, humidity, CBI, DangerClass, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.conn.execute(query, (timestamp, lat, log, alt, pre, temp, humidity, CBI, DangerClass, image_path))
            self.conn.commit()

            print("Walking mode data inserted.")
            LED.stop()
        except Exception as e:
            print(f"Error collecting walk data: {e}")
            

    def close_db(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
