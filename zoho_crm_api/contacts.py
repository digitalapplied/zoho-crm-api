from .client import ApiClient
from .utils import log_action, logging, ZohoApiError

def contact_exists(client: ApiClient, email: str):
    """
    Checks if a contact exists with the given email address.

    Args:
        client (ApiClient): An instance of the API client.
        email (str): The email address to search for.

    Returns:
        bool: True if a contact exists, False otherwise.

    Raises:
        ZohoApiError: If the API call fails for reasons other than 204.
    """
    if not email:
        log_action("Email address is empty, cannot check contact.", logging.WARNING)
        return False

    log_action(f"Checking for contact with email: {email}", logging.INFO)
    path = "/crm/v8/Contacts/search"
    params = {"email": email}

    try:
        response = client.make_request('GET', path, params=params)
        # Status Code 204 means No Content / Not Found for search by email/phone
        if response is None:
            log_action(f"No contact found for email: {email} (Status 204)", logging.INFO)
            return False
        # Check if response is a dictionary and has data
        elif isinstance(response, dict) and response.get("data"):
             log_action(f"Contact found for email: {email}", logging.INFO)
             return True
        else:
            # Log unexpected successful response structure if needed
            log_action(f"Contact existence check for {email} returned unexpected success response structure: {response}", logging.WARNING)
            return False # Or raise an error depending on how strict you want to be
    except ZohoApiError as e:
        # Specific handling might be needed, e.g., ignore certain errors?
        # For now, just log and re-raise.
        log_action(f"API error while checking contact {email}: {e}", logging.ERROR)
        raise # Re-raise the caught ZohoApiError
    except Exception as e:
        log_action(f"Unexpected error checking contact {email}: {str(e)}", logging.ERROR)
        raise # Re-raise any other unexpected error 