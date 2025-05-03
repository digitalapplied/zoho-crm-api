import os
import sys
import time

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from zoho_crm_api.client import ApiClient
from zoho_crm_api.leads import get_leads
from zoho_crm_api.contacts import contact_exists
from zoho_crm_api.tags import tag_lead
from zoho_crm_api.utils import log_action, logging, AuthError, ZohoApiError, ZohoApiException

# --- Configuration ---
LEAD_CUSTOM_VIEW_ID = os.getenv("LEAD_CV_ID", "1649349000008182385") # Example CV ID from .env or default
LEAD_FIELDS_TO_FETCH = "id,Email,First_Name,Last_Name"
DUPLICATE_TAG_NAME = "Duplicate in Contacts"
API_CALL_DELAY_SECONDS = 0.6 # Adjust as needed to respect rate limits
# ---

if __name__ == "__main__":
    start_time = time.time()
    processed_leads = 0
    duplicates_found = 0
    errors_encountered = 0

    try:
        log_action("Script started: Checking for duplicate contacts.", logging.INFO)
        print("Initializing API Client...")
        client = ApiClient()
        log_action("API Client initialized.", logging.INFO)

        print(f"\nGetting leads from Custom View ID: {LEAD_CUSTOM_VIEW_ID}...")
        log_action(f"Fetching leads from CV ID {LEAD_CUSTOM_VIEW_ID}.", logging.INFO)
        leads = get_leads(client, cvid=LEAD_CUSTOM_VIEW_ID, fields=LEAD_FIELDS_TO_FETCH)
        print(f"Found {len(leads)} leads.")
        log_action(f"Successfully fetched {len(leads)} leads.", logging.INFO)

        if not leads:
            print("No leads found in the specified custom view. Exiting.")
            log_action("No leads found. Script finished.", logging.INFO)
            exit()

        print("\nProcessing leads...")
        for lead in leads:
            processed_leads += 1
            email = lead.get("Email")
            lead_id = lead.get("id")
            lead_name = f"{lead.get('First_Name', '')} {lead.get('Last_Name', '')}".strip()

            print(f"\nProcessing lead {processed_leads}/{len(leads)}: ID {lead_id} ({lead_name})")

            if email:
                log_action(f"Checking lead {lead_id} ({lead_name}) with email: {email}", logging.INFO)
                try:
                    exists = contact_exists(client, email)
                    if exists:
                        duplicates_found += 1
                        print(f"  -> Contact EXISTS for email: {email}. Tagging lead...")
                        log_action(f"Contact exists for email: {email}. Tagging lead {lead_id}.", logging.INFO)
                        tag_lead(client, lead_id, tag_name=DUPLICATE_TAG_NAME)
                        log_action(f"Tagged lead {lead_id} as duplicate.", logging.INFO)
                        print(f"  -> Tagged lead {lead_id}.")
                    else:
                        print(f"  -> No matching contact for: {email}")
                        log_action(f"No matching contact for: {email} (Lead ID: {lead_id})", logging.INFO)

                except ZohoApiError as api_err:
                    errors_encountered += 1
                    print(f"  -> ERROR checking/tagging contact for lead {lead_id}: {api_err.status_code} - {api_err.error_response}")
                    log_action(f"API Error processing lead {lead_id}: {api_err}", logging.ERROR)
                except Exception as inner_e:
                    errors_encountered += 1
                    print(f"  -> ERROR processing lead {lead_id}: {str(inner_e)}")
                    log_action(f"Unexpected Error processing lead {lead_id}: {str(inner_e)}", logging.ERROR)

            else:
                print(f"  -> Lead {lead_id} ({lead_name}) has no email. Skipping check.")
                log_action(f"Lead {lead_id} ({lead_name}) has no email. Skipping.", logging.WARNING)

            # Add delay to manage rate limits
            time.sleep(API_CALL_DELAY_SECONDS)

    except AuthError as auth_e:
        print(f"\nFATAL: Authentication Error - {auth_e.message}")
        log_action(f"Authentication Error: {auth_e.message}", logging.CRITICAL)
        errors_encountered +=1
    except ZohoApiError as api_e:
         print(f"\nFATAL: Zoho API Error - {api_e.status_code}: {api_e.error_response}")
         log_action(f"Zoho API Error: {api_e}", logging.CRITICAL)
         errors_encountered +=1
    except ZohoApiException as base_e:
         print(f"\nFATAL: Zoho API Exception - {base_e.message}")
         log_action(f"Zoho API Exception: {base_e.message}", logging.CRITICAL)
         errors_encountered +=1
    except Exception as e:
        print(f"\nFATAL: An unexpected error occurred: {str(e)}")
        log_action(f"Unexpected script error: {str(e)}", logging.CRITICAL)
        errors_encountered += 1
    finally:
        end_time = time.time()
        duration = end_time - start_time
        summary = f"Script finished. Duration: {duration:.2f} seconds. Leads processed: {processed_leads}. Duplicates tagged: {duplicates_found}. Errors: {errors_encountered}."
        print(f"\n{summary}")
        log_action(summary, logging.INFO) 