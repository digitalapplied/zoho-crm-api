import datetime
import logging

# --- Custom Exceptions ---
class ZohoApiException(Exception):
    """Base exception for Zoho API related errors."""
    def __init__(self, message="An error occurred with the Zoho API"):
        self.message = message
        super().__init__(self.message)

class AuthError(ZohoApiException):
    """Exception raised for authentication errors."""
    def __init__(self, message="Authentication failed"):
        self.message = message
        super().__init__(self.message)

class ZohoApiError(ZohoApiException):
    """Exception raised for specific API errors returned by Zoho."""
    def __init__(self, status_code, error_response):
        self.status_code = status_code
        self.error_response = error_response
        # Try to extract a meaningful message from Zoho's error structure
        msg_detail = ""
        if isinstance(error_response, dict):
            msg_detail = error_response.get('message', str(error_response)) # Default to string representation
        else:
            msg_detail = str(error_response)

        message = f"Zoho API Error {status_code}: {msg_detail}"
        super().__init__(message)

# --- Logging Setup ---
# Default level is INFO. Change to logging.DEBUG to see more detailed logs.
logging.basicConfig(
    filename='process_log.log',
    level=logging.INFO, # Set default logging level here
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', # Added logger name
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Get a logger instance for this module
logger = logging.getLogger(__name__)

def log_action(message, level=logging.INFO):
    """Logs a message with a timestamp using the standard logging module."""
    # Map levels - you could expand this if needed
    if level == logging.DEBUG:
        logger.debug(message)
    elif level == logging.INFO:
        logger.info(message)
    elif level == logging.WARNING:
        logger.warning(message)
    elif level == logging.ERROR:
        logger.error(message)
    elif level == logging.CRITICAL:
        logger.critical(message)
    else: # Default to INFO if level is unknown
        logger.info(message)

# Example usage within other modules:
# from .utils import log_action, logging
# log_action("Something happened.", logging.INFO)
# log_action("Something went wrong!", logging.ERROR) 