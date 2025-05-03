import time
from .client import ApiClient
from .utils import log_action, logging, ZohoApiException

DEFAULT_FIELDS = "id,Email,First_Name,Last_Name"
MAX_RECORDS_PER_PAGE = 200

def get_leads(client: ApiClient, cvid: str, fields: str = DEFAULT_FIELDS):
    """
    Fetches leads from a specific custom view, handling pagination.

    Args:
        client (ApiClient): An instance of the API client.
        cvid (str): The Custom View ID.
        fields (str): Comma-separated string of field API names to retrieve.

    Returns:
        list: A list of lead dictionaries.

    Raises:
        ZohoApiException: If an API error occurs.
    """
    all_leads = []
    page_token = None
    page_num = 1 # For logging purposes

    params = {
        "cvid": cvid,
        "fields": fields,
        "per_page": MAX_RECORDS_PER_PAGE,
        # Start with page=1, remove it if page_token is used
        "page": 1
    }

    while True:
        log_action(f"Fetching leads page {page_num}. Using {'page_token' if page_token else 'page'} param.", logging.INFO)

        try:
            # Add page_token if available, remove page param
            if page_token:
                params["page_token"] = page_token
                params.pop("page", None) # Remove page if using token
            else:
                 params.pop("page_token", None) # Ensure page_token isn't carried over if expired/reset
                 params["page"] = page_num # Set page number for initial/non-token requests

            response_data = client.make_request('GET', '/crm/v8/Leads', params=params)

            if response_data is None: # Handle 204 No Content specifically if needed
                 log_action("Received no content for leads.", logging.INFO)
                 break

            if not isinstance(response_data, dict):
                 log_action(f"Unexpected response type: {type(response_data)}. Content: {response_data}", logging.ERROR)
                 raise ZohoApiException(f"Unexpected response format from leads API.")

            leads_page = response_data.get("data", [])
            if leads_page: # Check if the list is not empty
                 all_leads.extend(leads_page)
                 log_action(f"Fetched {len(leads_page)} leads on page {page_num}. Total fetched: {len(all_leads)}", logging.DEBUG)
            else:
                 log_action(f"No leads found on page {page_num}.", logging.DEBUG)

            info = response_data.get("info", {})
            if info.get("more_records"):
                page_token = info.get("next_page_token")
                if not page_token:
                    log_action("more_records is true, but next_page_token is missing. Stopping pagination.", logging.WARNING)
                    break
                page_num += 1
                time.sleep(0.5) # Add a small delay between pages
            else:
                log_action("No more records indicated by API.", logging.INFO)
                break

        except Exception as e: # Catch potential errors from make_request or data processing
            log_action(f"Error fetching leads page {page_num}: {str(e)}", logging.ERROR)
            # Depending on requirements, you might want to break or raise
            raise ZohoApiException(f"Failed to fetch leads: {str(e)}")

    log_action(f"Finished fetching leads. Total leads retrieved: {len(all_leads)}", logging.INFO)
    return all_leads 