import requests
from .auth import API_DOMAIN

def contact_exists(email, access_token):
    url = f"{API_DOMAIN}/crm/v8/Contacts/search"
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json"
    }
    params = {"email": email}
    try:
        res = requests.get(url, headers=headers, params=params)
        if res.status_code == 204:
            return False
        elif res.ok:
            return True
        else:
            res.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error checking contact: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        raise 