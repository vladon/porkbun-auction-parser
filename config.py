# Configuration settings for Porkbun auction parser

# Base URL for the auction pages
BASE_URL = "https://porkbun.com/auctions"

# Output CSV file name
OUTPUT_FILE = "porkbun_auctions.csv"

# Search parameters
SEARCH_QUERY = ""  # Empty string means no search filter (scrape all domains)
MAX_PAGES_LIMIT = None  # None means no limit (scrape all available pages)

# Available search form parameters (can be extended as needed)
SEARCH_PARAMS = {
    'q': '',  # Search query for domain names
    'tld': '',  # Filter by TLD
    'min_price': '',  # Minimum price filter
    'max_price': '',  # Maximum price filter
    'min_bids': '',  # Minimum number of bids
    'sortName': 'domain',  # Sort field (domain, tldName, endTime, startPrice, currentBid, bids, domainAge, revenue, visitors)
    'sortDirection': 'ascending'  # Sort direction (ascending, descending)
}

# Request settings
REQUEST_DELAY_MIN = 1.0  # Minimum delay between requests in seconds
REQUEST_DELAY_MAX = 3.0  # Maximum delay between requests in seconds

# Retry settings
MAX_RETRIES = 3
RETRY_DELAY = 5.0  # Seconds to wait before retrying

# Request headers to mimic a browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Pagination settings
DOMAINS_PER_PAGE = 100
MAX_PAGES_TO_PROCESS = 3000  # Safety limit to prevent infinite loops

# CSV headers
CSV_HEADERS = [
    'domain',
    'tld',
    'time_left',
    'starting_price',
    'current_bid',
    'bids_count',
    'domain_age',
    'revenue',
    'visitors'
]

# Progress bar settings
PROGRESS_BAR_WIDTH = 50
PROGRESS_UPDATE_INTERVAL = 10  # Update progress every N domains
AUTO_FLUSH_INTERVAL = 100  # Auto-flush CSV every N domains

# State saving settings
STATE_FILE = "scraping_state.json"