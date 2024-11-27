import sqlite3
from datetime import datetime

# This establishes a creation or connection to the FireEye Database
def connect_db(db_name='fireeye_data.db'):
    conn = sqlite3.connect(db_name)
    return conn

# This creates a table if it doesn't exist
def create_tables(conn):
    cursor = conn.cursor()
    
    # Creates Flights Table
    create_flights_query = """
    CREATE TABLE IF NOT EXISTS Flights(
        FlightID INTEGER PRIMARY KEY AUTOINCREMENT,				-- Unique Flight ID for each flight
        FlightNum TEXT,                                         -- Flight Number
        date DATE,                                              -- Date of flight
        start_time DATETIME,                                    -- Start time of flight
        end_time DATETIME,                                      -- End of flight, NULL initially
        duration INTEGER,                                       -- Duration of fligh, NULL initially
        datalink INTEGER,                                       -- Foreign key to Flight Data table
        FOREIGN KEY (datalink) REFERENCES Flight_Data(DataID)   -- Link to Flight Data Table
    );
    """
    
    create_flight_data_query = """
    CREATE TABLE IF NOT EXISTS Flight_Data(
        DataID INTEGER PRIMARY KEY AUTOINCREMENT,               -- Unique Data ID for each data entry
        FlightID INTEGER,                                       -- Foreign key linking to Flights table
        timestamp DATETIME,                                     -- Timestamp when data is recorded
        lat REAL,                                               -- Latitude
        log REAL,                                              -- Longitude
        alt REAL,                                               -- Altitude
        temp REAL,                                              -- Temperature
        humidity REAL,                                          -- Humidity
        image_path TEXT,                                        -- Path to image
        FORIEGN KEY (FlightID) REFERENCES Flights(FlightID)     -- Link to Flights Table
    );
    """
    
    cursor.execute(create_flights_query)
    cursor.execute(create_flight_data_query)
    conn.commit()

# Insert flight data into Fights table
def insert_flight(conn, FlightNum, date, start_time, datalink=None):
    cursor = conn.cursor()
    query="""
    INSERT INTO Flights (FlightNum, date, start_time, datalink)
    VALUES (?, ?, ?, ?)
    """
    cursor.execute(query, (FlightNum, date, start_time, datalink))
    conn.commit()
    
# Retrieves and inserts all the data into Flight_Data table
def insert_flight_data(conn, FlightID, timestamp, lat, log, alt, temp, humidity, image_path):
    
    cursor = conn.cursor()
    query = """
    INSERT INTO Flight_Data (FlightID, timestamp, lat, log, alt, temp, humidity, image_path)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(insert_query, (FlightID, timestamp, lat, log, alt, temp, humidity, image_path))
    conn.commit()
    
# Retrieves all the data for the specific run indicated
def get_flight_data(conn, FlightID):
    cursor = conn.cursor()
    query = "SELECT * FROM Flight_Data WHERE FlightID = ?"
    cursor.execute(query, (run_id,))
    return cursor.fetchall()

# Terminates database connection
def close_db(conn):
    conn.close()
    
