import requests
import json
from .auth import API_DOMAIN

def get_leads(access_token):
    url = f"{API_DOMAIN}/crm/v8/Leads"
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json"
    }
    params = {
        "cvid": "1649349000008182385",
        "fields": "id,Email,First_Name,Last_Name",
        "per_page": 200,
        "page": 1
    }
    all_leads = []
    while True:
        print(f"Making request to: {url}")
        print(f"Headers: {json.dumps(headers, indent=2)}")
        print(f"Params: {json.dumps(params, indent=2)}")
        res = requests.get(url, headers=headers, params=params)
        res.raise_for_status()
        data = res.json().get("data", [])
        all_leads.extend(data)
        info = res.json().get("info", {})
        if not info.get("more_records"):
            break
        params["page"] += 1
    return all_leads 