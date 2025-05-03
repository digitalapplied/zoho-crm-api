# Zoho CRM API Toolkit

This project provides a modular toolkit for interacting with the Zoho CRM API, allowing you to build scripts and tools for a variety of CRM automation and integration tasks.

## Features

- Modular Python package for Zoho CRM API
- Easily extendable: add new modules for different CRM objects (Leads, Contacts, Accounts, etc.)
- Example scripts for common tasks (e.g., duplicate checking)
- Environment variable configuration

## Prerequisites

- Python 3.13 or higher
- A Zoho CRM account with API access
- Zoho CRM API credentials (Client ID, Client Secret, and Refresh Token)

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd zoho-crm-api
```

### 2. Set Up Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# .\venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the provided `.env.template` to `.env` and fill in your credentials:

```bash
cp .env.template .env
```

Edit `.env`:

```
ZOHO_CLIENT_ID=your_client_id
ZOHO_CLIENT_SECRET=your_client_secret
ZOHO_REFRESH_TOKEN=your_refresh_token
```

### 5. Project Structure

```
zoho-crm-api/
│
├── zoho_crm_api/                # Main package directory
│   ├── __init__.py
│   ├── auth.py                  # Authentication logic
│   ├── leads.py                 # Lead-related functions
│   ├── contacts.py              # Contact-related functions
│   ├── tags.py                  # Tagging and label functions
│   └── utils.py                 # Logging, helpers, etc.
│
├── scripts/
│   └── check_duplicates.py      # Example script using the package
│
├── .env.template                # Template for environment variables
├── .env                         # (not committed)
├── requirements.txt
├── README.md
├── pyrightconfig.json
└── process_log.txt
```

## Usage

### Example: Check for Duplicate Contacts

Run the example script:

```bash
python scripts/check_duplicates.py
```

### Adding New Functionality

- Add new modules to `zoho_crm_api/` for other CRM objects or features (e.g., `accounts.py`, `deals.py`).
- Create new scripts in the `scripts/` directory that use the package modules.

## Contributing

Feel free to submit issues and enhancement requests!

## License

[Your chosen license]
