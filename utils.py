"""
Utility Functions

Contains helper functions for logging, error handling, and other reusable operations.
"""
from imports import *

log_file = "error_log.txt"

if not os.path.exists(log_file):
    with open(log_file, 'w') as file:
        file.write("Error Log\n=====================\n")

logging.basicConfig(
    filename=log_file,
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_error(exception):
    """This functoin logs errors and prints the error details"""
    error_message = traceback.format_exc()
    logging.error(error_message)
    print(f"Error occurred:\n{error_message}")