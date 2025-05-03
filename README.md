# Zoho CRM API Integration

This project provides a Python-based integration with the Zoho CRM API, allowing you to interact with your Zoho CRM instance programmatically.

## Features

- Authentication with Zoho CRM API using OAuth 2.0
- Fetching leads from custom views
- Checking for duplicate contacts
- Tagging leads as duplicates
- Comprehensive logging
- Rate limiting protection
- Error handling and reporting

## Prerequisites

- Python 3.7 or higher
- A Zoho CRM account
- API credentials (Client ID, Client Secret, and Refresh Token)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/zoho-crm-api.git
   cd zoho-crm-api
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Copy the `.env.template` file to `.env`:

   ```bash
   cp .env.template .env
   ```

2. Edit the `.env` file and add your Zoho CRM API credentials:

   ```
   # Zoho CRM API Credentials
   ZOHO_CLIENT_ID=your_client_id_here
   ZOHO_CLIENT_SECRET=your_client_secret_here
   ZOHO_REFRESH_TOKEN=your_refresh_token_here

   # Zoho URLs (Adjust if needed for non-US DC, see docs)
   ZOHO_ACCOUNTS_URL=https://accounts.zoho.com
   # Optional: Default API domain if not fetched from token response yet
   # ZOHO_API_DOMAIN=https://www.zohoapis.com

   # Optional: Lead Custom View ID for check_duplicates script
   # LEAD_CV_ID=your_lead_custom_view_id
   ```

## Usage

### Check for Duplicate Contacts

The `check_duplicates.py` script checks for leads that have matching email addresses in your contacts and tags them as duplicates.

```bash
python scripts/check_duplicates.py
```

The script will:

1. Fetch leads from the specified custom view
2. Check each lead's email against your contacts
3. Tag leads as duplicates if a matching contact is found
4. Log all actions and provide a summary at the end

## Note on Scopes

Ensure your API client registration includes the necessary scopes. For the `check_duplicates.py` script, you'll need at least:

- `ZohoCRM.modules.leads.READ` (to get leads)
- `ZohoCRM.modules.contacts.READ` (implicitly used by contact search)
- `ZohoSearch.securesearch.READ` (for searching contacts by email)
- `ZohoCRM.modules.leads.UPDATE` (to add tags to leads)

Adjust scopes based on the specific operations your scripts perform. Refer to the Zoho CRM API documentation for scope details for each endpoint.

## Rate Limiting

Be mindful of Zoho CRM API limits (credits per day, concurrent requests). The `check_duplicates.py` script includes a small delay (`API_CALL_DELAY_SECONDS`) between processing leads to help manage limits. Adjust this value as needed for your specific usage and CRM plan. For large-scale operations, consider using Zoho's Bulk APIs.

## Logging

The script logs all actions to `process_log.log` with timestamps and log levels. You can adjust the logging level in `utils.py` if needed.

## Error Handling

The script includes comprehensive error handling for:

- Authentication errors
- API errors
- Network issues
- Unexpected errors

All errors are logged with appropriate severity levels and included in the final summary.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Zoho CRM API Documentation
- Python Requests Library
- Python-dotenv
