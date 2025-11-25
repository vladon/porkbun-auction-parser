# Development Setup Guide

This guide provides step-by-step instructions for setting up the development environment for the Porkbun Auction Parser project.

## Prerequisites

- Python 3.6 or higher (tested with Python 3.13.9)
- Git (for version control)
- Internet connection (for scraping and package installation)

## Quick Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd porkbun-auction-parser
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Verify Installation
```bash
python test_scraper.py
```

## Detailed Setup Instructions

### Environment Verification

The project has been tested with:
- **Python Version:** 3.13.9 (compatible with 3.6+)
- **Requests:** 2.31.0
- **BeautifulSoup4:** 4.12.2

### Project Structure

```
porkbun-auction-parser/
├── venv/                    # Virtual environment
├── config.py               # Configuration settings
├── csv_writer.py           # CSV output handling
├── main.py                 # Main entry point (interactive)
├── progress_utils.py       # Progress tracking utilities
├── run_full_scraping.py    # Multithreaded scraping entry point
├── scraper.py              # Single-threaded scraper
├── scraper_mt.py           # Multi-threaded scraper
├── test_scraper.py         # Test script
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
└── DEVELOPMENT_SETUP.md   # This file
```

### Configuration

The scraper behavior can be configured in [`config.py`](config.py):

- **Base URL:** `https://porkbun.com/auctions`
- **Output File:** `porkbun_auctions.csv`
- **Rate Limiting:** 1-3 seconds between requests
- **Max Retries:** 3 attempts
- **Domains per Page:** 100

### Running the Scraper

#### Basic Usage (Interactive)
```bash
python main.py
```

#### Multithreaded Scraping (Faster)
```bash
python run_full_scraping.py
```

#### Quick Test
```bash
python test_scraper.py
```

### Features

- **Single-threaded scraping:** Safe, respectful scraping with rate limiting
- **Multi-threaded scraping:** Faster parallel processing (10 workers by default)
- **Advanced filtering:** Search by domain pattern, TLD, price range, bids
- **CSV output:** Structured data export with all domain information
- **Progress tracking:** Real-time progress bars and statistics
- **Error handling:** Robust retry mechanisms and graceful interruption
- **Resume capability:** State saving for interrupted scraping sessions

### Output Format

The scraper generates a CSV file with the following columns:
- `domain`: Full domain name
- `tld`: Top-level domain
- `time_left`: Auction time remaining
- `starting_price`: Initial auction price
- `current_bid`: Current highest bid
- `bids_count`: Number of bids placed
- `domain_age`: Age of the domain
- `revenue`: Revenue data (if available)
- `visitors`: Visitor statistics (if available)

### Development Notes

#### Rate Limiting
The scraper implements respectful scraping with:
- Random delays between 1-3 seconds per request
- Configurable retry mechanisms
- Proper browser headers

#### Error Handling
- Network timeouts and connection errors
- HTML structure changes
- Rate limiting detection
- Graceful interruption with Ctrl+C

#### Testing
Always test with a small sample first:
```bash
python test_scraper.py
```

This will scrape 2 pages and verify the output before running a full scrape.

### Troubleshooting

#### Common Issues

1. **Missing packages:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Virtual environment not activated:**
   ```bash
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Permission errors:**
   - Ensure write permissions in the project directory
   - Check antivirus software isn't blocking the script

4. **Connection issues:**
   - Check internet connection
   - Verify firewall settings
   - Try running with fewer concurrent threads

#### Performance Tips

- Use multithreaded version for faster scraping: `python run_full_scraping.py`
- Limit page count for testing: enter a number when prompted
- Monitor system resources during large scrapes

### Legal Considerations

This scraper is for educational and research purposes. Please:
- Respect the website's terms of service
- Use reasonable rate limiting
- Don't overload the server with excessive requests
- Consider the impact on the website's resources

### Support

For issues or questions:
1. Check this setup guide
2. Review the main [`README.md`](README.md)
3. Run the test script to verify functionality
4. Check error messages for specific issues

---

**Last Updated:** 2025-11-25  
**Tested With:** Python 3.13.9, Windows 11