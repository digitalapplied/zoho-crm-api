import requests
from .auth import API_DOMAIN

def tag_lead(lead_id, access_token):
    url = f"{API_DOMAIN}/crm/v8/Leads/actions/add_tags"
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json"
    }
    body = {
        "tags": [
            {"name": "Duplicate in Contacts"}
        ],
        "ids": [lead_id]
    }
    try:
        res = requests.post(url, headers=headers, json=body)
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error tagging lead: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        raise 