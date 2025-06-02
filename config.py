"""
Configuration constants for the Data Creation Tool
"""

# API Configuration
DEFAULT_API_ENDPOINT = 'https://api.example.com/data'  # Replace with actual endpoint
DEFAULT_API_HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_TOKEN'  # Replace with actual token
}

# App Configuration
PAGE_CONFIG = {
    'page_title': "Data Creation Tool",
    'page_icon': "🚀",
    'layout': "wide",
    'initial_sidebar_state': "expanded"
}

# Data Generation Limits
MAX_RECORDS = 100000
DEFAULT_RECORD_COUNT = 10
DEFAULT_BATCH_SIZE = 100
MAX_BATCH_SIZE = 1000

# Template-specific defaults
TEMPLATE_DEFAULTS = {
    'facility': {'base_name': 'STORE'},
    'item': {'prefix': 'ITEM'},
    'po': {
        'vendor_ids': 'VENDOR001,VENDOR002',
        'item_ids': 'ITEM001,ITEM002',
        'facility_id': 'FACILITY01'
    }
}
