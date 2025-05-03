import os
import sys
import time

# --- Path Setup ---
# This adds the parent directory (project root) to the Python path.
# This allows the script to import the 'zoho_crm_api' package when run directly.
# Alternatives:
# 1. Install the package: Navigate to project root in terminal and run `pip install .`
# 2. Run as module: Navigate to project root and run `python -m scripts.check_duplicates`
# Choose the alternative if you plan to distribute or reuse the package more formally.
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# ---

from zoho_crm_api.client import ApiClient
from zoho_crm_api.leads import get_leads
from zoho_crm_api.contacts import contact_exists
from zoho_crm_api.tags import tag_lead
from zoho_crm_api.utils import log_action, logging, AuthError, ZohoApiError, ZohoApiException

# --- Configuration ---
# Get Lead CV ID from environment variable, fallback to a default if not set
LEAD_CUSTOM_VIEW_ID = os.getenv("LEAD_CV_ID", "1649349000008182385") # Provide a sensible default or raise error if not set
LEAD_FIELDS_TO_FETCH = "id,Email,First_Name,Last_Name"
DUPLICATE_TAG_NAME = "Duplicate in Contacts"
API_CALL_DELAY_SECONDS = 0.6 # Delay between leads processed (adjust based on API limits)
# ---

if __name__ == "__main__":
    start_time = time.time()
    processed_leads = 0
    duplicates_found = 0
    errors_encountered = 0

    try:
        log_action("-------------------------------------", logging.INFO)
        log_action("Script started: Checking for duplicate contacts.", logging.INFO)
        log_action("-------------------------------------", logging.INFO)
        print("Script started...")

        print("Initializing API Client...")
        client = ApiClient()
        log_action("API Client initialized.", logging.INFO)
        print("API Client initialized.")

        # Access token is now handled internally by the client.

        print(f"\nGetting leads from Custom View ID: {LEAD_CUSTOM_VIEW_ID}...")
        log_action(f"Fetching leads from CV ID {LEAD_CUSTOM_VIEW_ID}.", logging.INFO)
        leads = get_leads(client, cvid=LEAD_CUSTOM_VIEW_ID, fields=LEAD_FIELDS_TO_FETCH)
        print(f"Found {len(leads)} leads.")
        log_action(f"Successfully fetched {len(leads)} leads.", logging.INFO)

        if not leads:
            print("No leads found in the specified custom view. Exiting.")
            log_action("No leads found. Script finished.", logging.INFO)
            exit()

        print(f"\nProcessing {len(leads)} leads (with {API_CALL_DELAY_SECONDS}s delay between checks)...")
        for i, lead in enumerate(leads):
            processed_leads += 1
            email = lead.get("Email")
            lead_id = lead.get("id")
            lead_name = f"{lead.get('First_Name', '')} {lead.get('Last_Name', '')}".strip()

            print(f"\n[{processed_leads}/{len(leads)}] Processing lead: ID {lead_id} ({lead_name})")

            if email:
                log_action(f"[{processed_leads}/{len(leads)}] Checking lead {lead_id} ({lead_name}) with email: {email}", logging.INFO)
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

                    # Delay after *successful* contact check/tag operation
                    time.sleep(API_CALL_DELAY_SECONDS)

                except ZohoApiError as api_err:
                    errors_encountered += 1
                    print(f"  -> ERROR checking/tagging contact for lead {lead_id}: {api_err.status_code} - {api_err.error_response}")
                    log_action(f"API Error processing lead {lead_id}: {api_err}", logging.ERROR)
                    # Optional: add a longer delay after an API error?
                    time.sleep(API_CALL_DELAY_SECONDS * 2) # e.g., double delay after error
                except Exception as inner_e:
                    errors_encountered += 1
                    print(f"  -> ERROR processing lead {lead_id}: {str(inner_e)}")
                    log_action(f"Unexpected Error processing lead {lead_id}: {str(inner_e)}", logging.ERROR)
                    time.sleep(API_CALL_DELAY_SECONDS * 2) # e.g., double delay after error

            else:
                print(f"  -> Lead {lead_id} ({lead_name}) has no email. Skipping check.")
                log_action(f"Lead {lead_id} ({lead_name}) has no email. Skipping.", logging.WARNING)
                # Apply the delay even if skipped to maintain consistent pacing
                time.sleep(API_CALL_DELAY_SECONDS)


    except AuthError as auth_e:
        print(f"\nFATAL: Authentication Error - {auth_e.message}")
        log_action(f"Authentication Error: {auth_e.message}", logging.CRITICAL)
        errors_encountered +=1
    except ZohoApiError as api_e:
         print(f"\nFATAL: Zoho API Error during initial setup or lead fetch - {api_e.status_code}: {api_e.error_response}")
         log_action(f"Zoho API Error: {api_e}", logging.CRITICAL)
         errors_encountered +=1
    except ZohoApiException as base_e:
         print(f"\nFATAL: Zoho API Exception during initial setup or lead fetch - {base_e.message}")
         log_action(f"Zoho API Exception: {base_e.message}", logging.CRITICAL)
         errors_encountered +=1
    except Exception as e:
        print(f"\nFATAL: An unexpected error occurred: {str(e)}")
        log_action(f"Unexpected script error: {str(e)}", logging.CRITICAL)
        errors_encountered += 1
        # raise # Re-raise to see traceback if needed during development
    finally:
        end_time = time.time()
        duration = end_time - start_time
        summary = f"Script finished. Duration: {duration:.2f} seconds. Leads processed: {processed_leads}. Duplicates tagged: {duplicates_found}. Errors encountered: {errors_encountered}."
        print(f"\n-------------------------------------")
        print(f"{summary}")
        print(f"-------------------------------------")
        log_action("-------------------------------------", logging.INFO)
        log_action(summary, logging.INFO)
        log_action("-------------------------------------", logging.INFO) 