from .client import ApiClient
from .utils import log_action, logging, ZohoApiException

DEFAULT_TAG_NAME = "Duplicate in Contacts"

def tag_lead(client: ApiClient, lead_id: str, tag_name: str = DEFAULT_TAG_NAME):
    """
    Adds a specific tag to a lead record.

    Args:
        client (ApiClient): An instance of the API client.
        lead_id (str): The ID of the lead to tag.
        tag_name (str, optional): The name of the tag to add.
                                    Defaults to DEFAULT_TAG_NAME.

    Raises:
        ZohoApiException: If the API call fails.
    """
    log_action(f"Attempting to tag lead {lead_id} with '{tag_name}'", logging.INFO)
    path = "/crm/v8/Leads/actions/add_tags"
    body = {
        "tags": [
            {"name": tag_name}
            # Zoho API allows specifying tag ID too, which might be more reliable
            # {"name": tag_name, "id": "your_tag_id_if_known"}
        ],
        "ids": [lead_id]
    }

    try:
        response = client.make_request('POST', path, json_data=body)
        # Optional: Check response details for success confirmation per ID
        if response and response.get("data"):
            first_result = response["data"][0]
            if first_result.get("status") == "success":
                log_action(f"Successfully tagged lead {lead_id} with '{tag_name}'.", logging.INFO)
            else:
                log_action(f"Tagging lead {lead_id} reported non-success status: {first_result.get('message', 'No message')}", logging.WARNING)
        elif response is None:
             log_action(f"Tagging lead {lead_id} returned no content.", logging.WARNING)
        else:
             log_action(f"Tagging lead {lead_id} returned unexpected response: {response}", logging.WARNING)

    except Exception as e:
        log_action(f"Error tagging lead {lead_id}: {str(e)}", logging.ERROR)
        raise # Re-raise the exception 