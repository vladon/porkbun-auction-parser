# Porkbun Auction Parser

A Python web scraper that extracts all domain auction data from [porkbun.com/auctions](https://porkbun.com/auctions) and saves it to a CSV file for easy analysis.

## Features

- Scrapes all auction pages (300+ pages with 286,000+ domains)
- Extracts complete domain information:
  - Domain name
  - Top-level domain (TLD)
  - Time left in auction
  - Starting price
  - Current bid
  - Number of bids
  - Domain age
  - Revenue data
  - Visitor statistics
- Advanced search and filtering capabilities:
  - Search by domain name pattern (q= parameter)
  - Filter by TLD (com, org, net, etc.)
  - Filter by price range (minimum/maximum price)
  - Filter by minimum number of bids
  - Sort by various fields (domain, price, bids, age, etc.)
  - Sort direction (ascending/descending)
- Configurable page limits for testing
- Rate limiting to avoid being blocked
- Error handling and retry mechanisms
- Progress tracking and statistics
- CSV output for easy spreadsheet viewing
- Test mode for validation
- Multithreading support for faster scraping

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the scraper with the following command:

```bash
python main.py
```

The script will:
1. Validate that all required packages are installed
2. Ask if you want to run a test first (recommended)
3. Scrape all auction pages with rate limiting
4. Save data to `porkbun_auctions.csv`
5. Validate the output file

### Advanced Options

#### Limit Pages for Testing

If you want to test with a limited number of pages:

```bash
python main.py
# When prompted, enter the number of pages to scrape
```

#### Skip Testing

If you want to go directly to full scraping:

```bash
python main.py
# When prompted for test, enter 'n'
```

### Multithreaded Scraping (Faster)

For faster scraping with multithreading (10 parallel workers):

```bash
python run_full_scraping.py
```


#### Search and Filtering

The scraper now supports advanced search and filtering capabilities:

- **Search Query**: Search for specific domain patterns using the `q=` parameter
- **TLD Filter**: Filter results by top-level domain (com, org, net, etc.)
- **Price Range**: Set minimum and maximum price filters
- **Bid Filter**: Filter by minimum number of bids
- **Sorting**: Sort results by various fields (domain, price, bids, age, etc.)
- **Page Limits**: Limit scraping to specific number of pages for testing

When you run the scraper, you'll be prompted to enter these parameters:

```bash
python main.py
# Follow the interactive prompts to set search criteria
```

#### Search Examples

Here are some examples of how you can use the search features:

1. **Search for specific domains**:
   - Search query: `test`
   - This will find all domains containing "test"

2. **Filter by TLD**:
   - TLD filter: `com`
   - This will only show .com domains

3. **Price range filtering**:
   - Minimum price: `100`
   - Maximum price: `1000`
   - This will show domains with bids between $100 and $1000

4. **Sort by current bid (descending)**:
   - Sort field: `5` (currentBid)
   - Sort direction: `desc`
   - This will show highest bid domains first
This significantly speeds up the scraping process while maintaining rate limiting per thread.

### Progress Bar and Auto-Flush Features

The scraper now includes enhanced user feedback and data safety features:

- **Real-time Progress Bar**: Shows current scraping progress with percentage and ETA
- **Auto-Flush to Disk**: Automatically saves data to disk at intervals to prevent data loss
- **State Management**: Saves scraping state for resumption after interruption
- **Configurable Intervals**: Progress updates and auto-flush intervals are configurable

These features ensure:
- Better visibility into scraping progress
- Data safety with periodic disk writes
- Ability to resume interrupted scraping sessions
- Reduced risk of data loss from crashes or interruptions

## Output

The scraper creates a CSV file named `porkbun_auctions.csv` with the following columns:

- `domain`: The full domain name
- `tld`: Top-level domain (e.g., com, org, net)
- `time_left`: Time remaining in the auction
- `starting_price`: Initial auction price
- `current_bid`: Current highest bid
- `bids_count`: Number of bids placed
- `domain_age`: Age of the domain
- `revenue`: Revenue data (if available)
- `visitors`: Visitor statistics (if available)

## Configuration

You can modify the scraping behavior by editing `config.py`:

- `REQUEST_DELAY_MIN/MAX`: Adjust delay between requests (1-3 seconds default)
- `MAX_RETRIES`: Number of retry attempts for failed requests
- `OUTPUT_FILE`: Change the output filename
- `MAX_PAGES_TO_PROCESS`: Safety limit for maximum pages

## Rate Limiting

The scraper implements rate limiting to avoid being blocked:
- Random delays between 1-3 seconds per request

- **Multithreaded version**: 5-10x faster with 10 parallel workers
- Retry mechanism for failed requests
- Proper browser headers to mimic legitimate traffic

## Performance

- **Expected duration**: Several hours for full scraping (due to rate limiting)
- **Data volume**: ~286,000+ domains across 300+ pages
- **File size**: Approximately 10-20MB CSV file

## Error Handling

The scraper includes comprehensive error handling:
- Network timeouts and connection errors
- HTML structure changes
- Rate limiting detection
- Incomplete data handling
- Graceful interruption with Ctrl+C

## Troubleshooting

### Common Issues

1. **Missing packages**: Run `pip install -r requirements.txt`
2. **Connection errors**: Check internet connection and try again
3. **Rate limiting**: The scraper will automatically retry after delays
4. **Interruption**: If interrupted, the CSV file will contain data up to that point

### Resume Functionality

If the scraper is interrupted, you can:
1. Check the existing CSV file for data collected so far
2. Run the scraper again (it will append to existing file)
3. Use page limiting to continue from where you left off

## Legal Considerations

This scraper is for educational and research purposes. Please:
- Respect the website's terms of service
- Use reasonable rate limiting
- Don't overload the server with excessive requests
- Consider the impact on the website's resources

## Requirements

- Python 3.6 or higher
- Internet connection
- Required packages (see requirements.txt)

## License

This project is for educational purposes. Use responsibly and in accordance with the target website's terms of service.