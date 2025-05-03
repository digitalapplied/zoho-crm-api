import os
import time
import requests
from dotenv import load_dotenv
from .utils import log_action, logging, AuthError

load_dotenv()

# Load credentials and URLs from environment variables
CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")
CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN")
ACCOUNTS_URL = os.getenv("ZOHO_ACCOUNTS_URL", "https://accounts.zoho.com") # Default to US
DEFAULT_API_DOMAIN = os.getenv("ZOHO_API_DOMAIN", "https://www.zohoapis.com") # Default to US

# --- In-memory token storage (replace with persistent storage if needed) ---
# This dictionary will hold the current token info.
# WARNING: This is NOT persistent. Token will be lost if script restarts.
# Consider using a file or database for persistence in production.
_token_data = {
    "access_token": None,
    "expires_at": 0,        # Store expiry time as a Unix timestamp
    "api_domain": DEFAULT_API_DOMAIN
}
# ---

def _refresh_access_token():
    """Internal function to refresh the access token using the refresh token."""
    log_action("Attempting to refresh access token...", logging.INFO)
    if not REFRESH_TOKEN or not CLIENT_ID or not CLIENT_SECRET:
        msg = "Missing ZOHO_CLIENT_ID, ZOHO_CLIENT_SECRET, or ZOHO_REFRESH_TOKEN in environment variables."
        log_action(msg, logging.ERROR)
        raise AuthError(msg)

    params = {
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
    }
    token_url = f"{ACCOUNTS_URL}/oauth/v2/token"

    try:
        res = requests.post(token_url, params=params)
        res.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = res.json()

        if "access_token" in data:
            _token_data["access_token"] = data["access_token"]
            expires_in = data.get("expires_in", 3600)  # Default to 1 hour if not provided
            # Calculate expiry timestamp (with a 60-second buffer)
            _token_data["expires_at"] = time.time() + expires_in - 60
            # Store the API domain provided in the response
            _token_data["api_domain"] = data.get("api_domain", DEFAULT_API_DOMAIN)
            log_action(f"Access token refreshed successfully. Valid until: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(_token_data['expires_at']))}. API Domain: {_token_data['api_domain']}", logging.INFO)
            return _token_data["access_token"]
        else:
            error_msg = f"Failed to refresh token. 'access_token' not in response. Response: {data}"
            log_action(error_msg, logging.ERROR)
            raise AuthError(error_msg)

    except requests.exceptions.RequestException as e:
        error_details = f"Network/Request Error during token refresh: {str(e)}"
        if hasattr(e.response, 'status_code'):
            error_details += f" | Status: {e.response.status_code}"
        if hasattr(e.response, 'text'):
            # Try to parse Zoho's error JSON if available
            try:
                zoho_error = e.response.json()
                error_details += f" | Response Body: {zoho_error}"
            except requests.exceptions.JSONDecodeError:
                 error_details += f" | Response Body: {e.response.text}" # Log raw text if not JSON
        log_action(error_details, logging.ERROR)
        # Specific check for common OAuth errors
        if hasattr(e.response, 'status_code') and e.response.status_code == 400:
             raise AuthError(f"Invalid client configuration or refresh token: {error_details}")
        raise AuthError(error_details) # General auth error for other request issues
    except Exception as e: # Catch any other unexpected errors like JSON parsing errors if response was malformed but status 200
        log_action(f"Unexpected error during token refresh processing: {str(e)}", logging.ERROR)
        raise AuthError(f"Unexpected error processing token refresh: {str(e)}")


def get_access_token():
    """
    Retrieves the current access token.
    Refreshes the token if it's missing or expired.
    """
    current_time = time.time()
    if _token_data["access_token"] and _token_data["expires_at"] > current_time:
        log_action("Using existing valid access token.", logging.DEBUG) # Uncommented DEBUG log
        return _token_data["access_token"]
    else:
        if not _token_data["access_token"]:
            log_action("Access token is missing. Refreshing...", logging.INFO)
        else:
             log_action("Access token has expired. Refreshing...", logging.INFO)
        return _refresh_access_token()

def get_api_domain():
    """Returns the API domain associated with the current token."""
    # Ensure token is refreshed if needed, which also updates api_domain
    get_access_token()
    return _token_data.get("api_domain", DEFAULT_API_DOMAIN) # Fallback just in case 