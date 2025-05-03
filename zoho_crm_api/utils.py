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
        message = f"Zoho API Error {status_code}: {error_response}"
        super().__init__(message)

# --- Logging Setup ---
logging.basicConfig(
    filename='process_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_action(message, level=logging.INFO):
    """Logs a message with a timestamp."""
    if level == logging.ERROR:
        logging.error(message)
    elif level == logging.WARNING:
        logging.warning(message)
    else:
        logging.info(message) 