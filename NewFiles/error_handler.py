# Importing Libraries
import traceback
import logging

# Importing Modules
from datetime import datetime

# Configure Logging
logging.basicConfig(filename="error_log.txt", level=logging.ERROR, format="%(asctime)s - %(message)s")

def log_error(error_message, function_name=None):
    """
    Logs an error with details

    Args:
        error_message (str): The error message.
        function_name (str, optional): The name of the function where the error occured
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    function_info = f" in {function_name}" if function_name else ""

    log_message = f"[{timestamp}] Error{function_info}: {error_message}"

    # Prints error messasge for debugging
    print(log_message)

    # Writes it into log file
    logging.error(log_message)