import requests
import json
from . import auth
from .utils import log_action, logging, ZohoApiError, AuthError, ZohoApiException

class ApiClient:
    """Handles making requests to the Zoho CRM API."""

    def __init__(self):
        # Initialization logic if needed, e.g., loading base URL
        pass

    def _get_headers(self):
        """Constructs the authorization header."""
        try:
            access_token = auth.get_access_token()
            return {
                "Authorization": f"Zoho-oauthtoken {access_token}",
                "Content-Type": "application/json" # Default content type
            }
        except AuthError as e:
            # Propagate AuthError if token retrieval fails
            raise e

    def make_request(self, method, path, params=None, json_data=None, data=None, headers=None, files=None):
        """
        Makes an API request to Zoho CRM.

        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE).
            path (str): API endpoint path (e.g., '/crm/v8/Leads').
            params (dict, optional): URL parameters. Defaults to None.
            json_data (dict, optional): JSON body for POST/PUT. Defaults to None.
            data (dict, optional): Form data for POST/PUT. Defaults to None.
            headers (dict, optional): Additional headers. Defaults to None.
            files (dict, optional): Files for multipart upload. Defaults to None.

        Returns:
            dict or None: Parsed JSON response or None for 204 status.

        Raises:
            AuthError: If authentication fails during header generation.
            ZohoApiError: If the API returns an error status code.
            requests.exceptions.RequestException: For network or request issues.
        """
        api_domain = auth.get_api_domain()
        url = f"{api_domain}{path}"
        request_headers = self._get_headers() # Handles AuthError internally

        if headers:
            request_headers.update(headers)

        # Clean up Content-Type if files are present (requests handles it)
        if files:
            request_headers.pop("Content-Type", None)

        log_action(f"Making {method} request to {url}", logging.DEBUG)
        if params: log_action(f"Params: {json.dumps(params)}", logging.DEBUG)
        if json_data: log_action(f"JSON Body: {json.dumps(json_data)}", logging.DEBUG)
        if data: log_action(f"Form Data: {data}", logging.DEBUG) # Be careful logging sensitive form data

        try:
            res = requests.request(
                method,
                url,
                headers=request_headers,
                params=params,
                json=json_data,
                data=data, # Use data for form-encoded
                files=files
            )

            log_action(f"Response Status Code: {res.status_code}", logging.DEBUG)

            if res.status_code == 204:  # No Content
                log_action("Received 204 No Content.", logging.INFO)
                return None
            elif res.ok:  # Includes 200, 201, 202
                try:
                    response_json = res.json()
                    log_action("Request successful.", logging.INFO)
                    return response_json
                except json.JSONDecodeError:
                    log_action("Request successful but failed to decode JSON response.", logging.WARNING)
                    # Return raw text if JSON decoding fails but status is OK
                    return res.text
            else:
                # Handle API errors (4xx, 5xx)
                try:
                    error_json = res.json()
                    log_action(f"API Error {res.status_code}: {json.dumps(error_json)}", logging.ERROR)
                    raise ZohoApiError(res.status_code, error_json)
                except json.JSONDecodeError:
                    log_action(f"API Error {res.status_code}: Failed to decode error JSON. Response text: {res.text}", logging.ERROR)
                    raise ZohoApiError(res.status_code, {"message": f"Non-JSON error response: {res.text}"})

        except requests.exceptions.RequestException as e:
            log_action(f"Network/Request Error: {str(e)}", logging.ERROR)
            raise  # Re-raise the original network error
        except ZohoApiError as e:
            raise # Re-raise Zoho specific API errors
        except AuthError as e:
             raise # Re-raise Auth errors
        except Exception as e:
            # Catch any other unexpected errors during the request process
            log_action(f"Unexpected error during request: {str(e)}", logging.ERROR)
            raise ZohoApiException(f"Unexpected error: {str(e)}") 