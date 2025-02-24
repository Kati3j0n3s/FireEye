# Standard Libraries
import traceback
import logging
from datetime import datetime

# Configure Logging
logging.basicConfig(filename="error_log.txt", level=logging.ERROR, format="%(asctime)s - %(message)s")

def log_error(error_message, function_name=None):
    """
    Logs an error with details, including the stack trace.

    Args:
        error_message (str): The error message.
        function_name (str, optional): The name of the function where the error occured
    """

    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # If function is passed, include it in the message
    function_info = f" in {function_name}" if function_name else ""

    # Prepare the log message
    log_message = f"[{timestamp}] Error{function_info}: {error_message}"

    # Capture the full stack trace of the exception
    stack_trace = traceback.format_exc()

    # Final log messages including stack trace
    log_message += f"\nStack Trace:\n{stack_trace}"

    # Prints error messasge for debugging
    print(log_message)

    # Writes it into log file
    logging.error(log_message)