import sqlite3
from datetime import datetime

# This establishes a connection to the FireEye Database
# CURRENTLY NOT CREATED
def connect_db(db_name='fireeye_data.db'):
    conn = sqlite3.connect(db_name)
    return conn

# This creates a table if it doesn't exist
def create_run_table(conn):
    cursor = conn.cursor()
    # Creates a table if it doesn't exist, make sure to add any additions when implemented
    create_table_query = """
    CREATE TABLE IF NOT EXISTS sensor_data(
        id INTEGER PRIMARY KEY AUTOINCREMENT,					-- Unique identifier for each entry
        run_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 		-- Timestamp of the pass/run
        temperature REAL,										-- Temperature reading
        humidity REAL,											-- Humidity reading
        run_id TEXT,											-- Unique ID for each run, timestamp or UUID
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    
# Retrieves and inserts all the data into database
def insert_sensor_data(conn, temperature, humidity, run_id):
    cursor = conn.cursor()
    query = """
    INSERT INTO sensor_data (temperature, humidity, run_id)
    VALUES (?, ?, ?)
    """
    cursor.execute(insert_query, (temperature, humidity, run_id))
    conn.commit()
    
# Retrieves all the data for the specific run indicated
def get_data_by_run(conn, run_id):
    cursor = conn.cursor()
    query = "SELECT * FROM sensor_data WHERE run_id = ?"
    cursor.execute(query, (run_id,))
    return cursor.fetchall()

# Terminates database connection
def close_db(conn):
    conn.close()
    