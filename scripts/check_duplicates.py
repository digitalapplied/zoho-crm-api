from zoho_crm_api.auth import get_access_token
from zoho_crm_api.leads import get_leads
from zoho_crm_api.contacts import contact_exists
from zoho_crm_api.tags import tag_lead
from zoho_crm_api.utils import log_action

if __name__ == "__main__":
    try:
        print("Getting access token...")
        token = get_access_token()
        print("Access token obtained successfully")
        log_action("Access token obtained successfully")
        
        print("\nGetting leads...")
        leads = get_leads(token)
        print(f"Found {len(leads)} leads")
        log_action(f"Found {len(leads)} leads from custom view 1649349000008182385")

        for lead in leads:
            email = lead.get("Email")
            lead_id = lead.get("id")
            if email:
                log_action(f"Checking lead {lead_id} with email: {email}")
                if contact_exists(email, token):
                    print(f"Contact already exists for email: {email}")
                    log_action(f"Contact exists for email: {email}. Tagging lead {lead_id}.")
                    tag_lead(lead_id, token)
                    log_action(f"Tagged lead {lead_id} as duplicate.")
                else:
                    print(f"No matching contact for: {email}")
                    log_action(f"No matching contact for: {email}")
            else:
                log_action(f"Lead {lead_id} has no email. Skipping.")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        log_action(f"Error occurred: {str(e)}")
        raise 