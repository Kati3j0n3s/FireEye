import sqlite3
import LED
import os

from Diagnostic import *
from ReadData import *
from datetime import datetime
from CameraData import *
from picamzero import *


sensor_id = check_ds18b20_sensor()

DATABASE_PATH = '/home/username/FireEye GitHub/FireEye/fireeye_data.db'

# This establishes a creation or connection to the FireEye Database
def connect_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute('PRAGMA journal_mode=WAL;')
    return conn

# This creates a table if it doesn't exist
def create_tables(conn):
    cursor = conn.cursor()
    
    # cursor.execute("DROP TABLE IF EXISTS Flights")
    # cursor.execute("DROP TABLE IF EXISTS Flight_Data")
    
    # Creates Flights Table
    create_flights_query = """
    CREATE TABLE IF NOT EXISTS Flights(
        FlightID INTEGER PRIMARY KEY AUTOINCREMENT,				-- Unique Flight ID for each flight
        FlightName TEXT,                                        -- Flight Name
        date DATE,                                              -- Date of flight
        start_time DATETIME,                                    -- Start time of flight
        end_time DATETIME,                                      -- End of flight, NULL initially
        duration INTEGER                                        -- Duration of fligh, NULL initially
    );
    """
    # Creates Flight_Data Table
    create_flight_data_query = """
    CREATE TABLE IF NOT EXISTS Flight_Data(
        DataID INTEGER PRIMARY KEY AUTOINCREMENT,               -- Unique Data ID for each data entry
        FlightID INTEGER,                                       -- Foreign key linking to Flights table
        timestamp DATETIME,                                     -- Timestamp when data is recorded
        lat REAL,                                               -- Latitude
        log REAL,                                               -- Longitude
        alt REAL,                                               -- Altitude
        pre REAL,                                               -- Pressure
        temp REAL,                                              -- Temperature
        humidity REAL,                                          -- Humidity
        CBI REAL,                                               -- CBI Calculation
        DangerClass TEXT,                                       -- Fire Danger Class indication
        image_path TEXT                                         -- Path to image
    );
    """
    
    create_walk_data_query = """
    CREATE TABLE IF NOT EXISTS Walk_Data(
        DataID INTEGER PRIMARY KEY AUTOINCREMENT,               -- Unique Data ID for each data entry
        timestamp DATETIME,                                     -- Timestamp when data is recorded
        lat REAL,                                               -- Latitude
        log REAL,                                               -- Longitude
        alt REAL,                                               -- Altitude
        pre REAL,                                               -- Pressure
        temp REAL,                                              -- Temperature
        humidity REAL,                                          -- Humidity
        CBI REAL,                                               -- CBI Calculation
        DangerClass TEXT,                                       -- Fire Danger Class Indication
        image_path TEXT                                         -- Path to image
    );
    """
    
    cursor.execute(create_flights_query)
    cursor.execute(create_flight_data_query)
    cursor.execute(create_walk_data_query)
    conn.commit()

# Insert flight data into Fights table
def insert_flight(conn, FlightName, date, start_time):
    cursor = conn.cursor()
    query="""
    INSERT INTO Flights (FlightName, date, start_time)
    VALUES (?, ?, ?)
    """
    cursor.execute(query, (FlightName, date, start_time))
    conn.commit()
    
    
    return cursor.lastrowid
    
# Retrieves and inserts all the data into Flight_Data table
def insert_flight_data(conn, FlightID, timestamp, lat, log, alt, pre, temp, humidity, CBI, DangerClass, image_path):
    
    cursor = conn.cursor()
    query = """
    INSERT INTO Flight_Data (FlightID, timestamp, lat, log, alt, pre, temp, humidity, CBI, DangerClass, image_path)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (FlightID, timestamp, lat, log, alt, pre, temp, humidity, CBI, DangerClass, image_path))
    conn.commit()
    
# Updates Flight with end_time and duration
def complete_flight(conn, FlightID, end_time):
    cursor = conn.cursor()
    query = """
    UPDATE Flights
    SET end_time = ?, duration = ?
    WHERE FlightID = ?
    """
    
    # Fetch start_time for the given FlightID
    start_time_query = "SELECT start_time FROM Flights WHERE FlightID = ?"
    cursor.execute(start_time_query, (FlightID,))
    result = cursor.fetchone()
    
    if result is None:
        raise ValueError(f"No flight found with FlightID {FlightID}")
        
    start_time = datetime.fromisoformat(result[0])
    
    duration = (end_time - start_time).total_seconds()
    print("duration added.")
    cursor.execute(query, (end_time, duration, FlightID))
    conn.commit()
    
# This simulates collecting data every time.sleep(number of seconds) for total of number of seconds * range(num)
# Basically, multiply the time.sleep value by range value and you get total collection time.
def collect_flight_data(conn, barometer_sensor, camera, interval = 20, i = 0): # 20 Sec intervals
    # Creating directory for saved images
    base_image_directory = "/home/username/FireEye GitHub/FireEye/FireEye Images"
    
    if not os.path.exists(base_image_directory):
        os.makedirs(base_image_directory)
    
    flight_name = f"Flight {str(conn.execute('SELECT COUNT(*) FROM Flights').fetchone()[0] + 1).zfill(3)}"
    print("flight_name added.")
    date = datetime.now().date()
    print("date added.")
    start_time = datetime.now()
    print("start_time added.")
    
    # Create a directory for the flight's images
    flight_image_directory = os.path.join(base_image_directory, flight_name)
    os.makedirs(flight_image_directory, exist_ok=True)
    
    # Insert a new flight record
    flight_id = insert_flight(conn, flight_name, date, start_time)
    
    # Data Collection
    timestamp = datetime.now()
    print("timestamp added.")
    lat = 0.01
    print("lat added.")
    log = 0.00
    print("log added.")
    alt = read_alt(barometer_sensor)
    print("alt added.")
    pre = read_pre(barometer_sensor)
    print("pre added.")
    temp = read_temp(sensor_id)
    print("temp added.")
    humidity = hum_main()
    print("hum added.")

    # Generate the image path
    image_name = f"image_{i}_{timestamp.strftime('%Y%m%d_%H%M%S')}.jpg"
    image_path = os.path.join(flight_image_directory, image_name)
        
    # Capture an image using the take_picture function
    try:
        if take_picture(camera, image_path):
            print(f"Image successfully saved: {image_path}")
        else:
            print(f"Failed to save image: {image_path}")
    except Exception as e:
        print(f"Error capturing image: {e}")
        image_path = None
            
    # Calculate CBI and give Danger Class
    CBI = calculate_cbi(temp, humidity)
    print("CBI added.")
        
    # Determine Danger Class
    DangerClass = determine_danger_class(CBI)
    print("DangerClass added.")
        
        
    insert_flight_data(conn, flight_id, timestamp, lat, log, alt, pre, temp, humidity, CBI, DangerClass, image_path)
    print("Inserted data.")
    
    time.sleep(interval)
    
    return flight_id
    
    
    
def collect_walk_data(conn, barometer_sensor, camera):
    LED.stop()
    LED.pulse('yellow')
    # Creating directory for saved images
    base_image_directory = "/home/username/FireEye GitHub/FireEye/FireEye Images"
    
    if not os.path.exists(base_image_directory):
        os.makedirs(base_image_directory)
    
    # Data Collection
    timestamp = datetime.now()
    print("timestamp added.")
    lat = 0.00
    print("lat added.")
    log = 0.00
    print("log added.")
    alt = read_alt(barometer_sensor)
    print("alt added.")
    pre = read_pre(barometer_sensor)
    print("pre added.")
    temp = read_temp(sensor_id)
    print("temp added.")
    humidity = hum_main()
    print("hum added.")

    # Generate the image path
    image_name = f"walk_image_{timestamp.strftime('%Y%m%d_%H%M%S')}.jpg"
    image_path = os.path.join(base_image_directory, image_name)
    
    # Capture an image using the take_picture function
    try:
        if take_picture(camera, image_path):
            print(f"Image successfully saved: {image_path}")
        else:
            print(f"Failed to save image: {image_path}")
    except Exception as e:
        print(f"Error capturing image: {e}")
        image_path = None
        
    # Calculate CBI and give Danger Class
    CBI = calculate_cbi(temp, humidity)
    print("CBI added.")
        
    # Determine Danger Class
    DangerClass = determine_danger_class(CBI)
    print("DangerClass added.")
    
    # Insert into Walk_Data Table
    cursor = conn.cursor()
    query = """
    INSERT INTO Walk_Data (timestamp, lat, log, alt, pre, temp, humidity, CBI, DangerClass, image_path)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, (timestamp, lat, log, alt, pre, temp, humidity, CBI, DangerClass, image_path))
    conn.commit()
    
    print("Walking Mode data collected and inserted successfully")
    LED.stop()
    
# Terminates database connection
def close_db(conn):
    conn.close()
