#!/usr/bin/env python3
"""
Porkbun Auction Parser
Scrapes all domain auction data from porkbun.com/auctions and saves to CSV
"""

import sys
import os
from datetime import datetime
from scraper import PorkbunScraper
from csv_writer import CSVWriter
from config import SEARCH_PARAMS

def print_banner():
    """Print the application banner"""
    print("=" * 60)
    print("    Porkbun Auction Parser")
    print("    Scraping all domain auction data from porkbun.com")
    print("=" * 60)
    print()

def validate_environment():
    """Validate that the environment is set up correctly"""
    try:
        import requests
        import bs4
        print("✓ All required packages are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def test_scraper(scraper, csv_writer, max_pages=2):
    """Test the scraper with a small sample of pages"""
    print("\n" + "=" * 40)
    print("TESTING SCRAPER WITH SAMPLE PAGES")
    print("=" * 40)
    
    test_domains = []
    current_offset = 0
    
    for page in range(max_pages):
        print(f"\nTesting page {page + 1}...")
        domains, _ = scraper.scrape_page(current_offset)
        
        if domains is None:
            print("✗ Failed to scrape test page")
            return False
            
        if not domains:
            print("✗ No domains found on test page")
            return False
            
        test_domains.extend(domains)
        
        # Write test data to CSV
        success_count = csv_writer.write_multiple_domains(domains)
        print(f"✓ Successfully wrote {success_count} domains to CSV")
        
        current_offset += 100
        
        # Add delay between test pages
        if page < max_pages - 1:
            import time
            time.sleep(2)
    
    print(f"\n✓ Test completed successfully!")
    print(f"✓ Total test domains scraped: {len(test_domains)}")
    
    # Show sample data
    if test_domains:
        print("\nSample domain data:")
        sample = test_domains[0]
        for key, value in sample.items():
            print(f"  {key}: {value}")
    
    return True

def run_full_scraping(scraper, csv_writer, max_pages=None):
    """Run the full scraping process"""
    print("\n" + "=" * 40)
    print("STARTING FULL SCRAPING PROCESS")
    print("=" * 40)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if max_pages:
        print(f"Limiting to {max_pages} pages for testing")
    
    try:
        # Scrape all pages
        all_domains, total_domains = scraper.scrape_all_pages(max_pages)
        
        # Write all data to CSV
        if all_domains:
            success_count = csv_writer.write_multiple_domains(all_domains)
            print(f"\n✓ Successfully wrote {success_count} domains to CSV")
            
            # Show statistics
            stats = scraper.get_scraping_stats()
            print(f"\nFinal Statistics:")
            print(f"  Total domains scraped: {stats['total_domains_scraped']}")
            print(f"  Total pages scraped: {stats['total_pages_scraped']}")
            print(f"  Total errors: {stats['error_count']}")
            
            if total_domains:
                completion_rate = (stats['total_domains_scraped'] / total_domains) * 100
                print(f"  Completion rate: {completion_rate:.2f}%")
                
        else:
            print("✗ No domains were scraped")
            return False
            
    except KeyboardInterrupt:
        print("\n\n⚠ Scraping interrupted by user")
        stats = scraper.get_scraping_stats()
        print(f"Progress so far: {stats['total_domains_scraped']} domains from {stats['total_pages_scraped']} pages")
        return False
        
    except Exception as e:
        print(f"\n✗ Error during scraping: {e}")
        return False
    
    print(f"\nEnd time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return True

def get_search_parameters():
    """Get search parameters from user input"""
    print("\n" + "=" * 40)
    print("SEARCH PARAMETERS (optional)")
    print("=" * 40)
    print("Leave blank to skip any parameter")
    
    params = {}
    
    # Search query
    search_query = input("Enter search query (domain name pattern): ").strip()
    if search_query:
        params['q'] = search_query
    
    # TLD filter
    tld = input("Filter by TLD (e.g., com, org, net): ").strip()
    if tld:
        params['tld'] = tld
    
    # Price range
    min_price = input("Minimum price (leave blank for no minimum): ").strip()
    if min_price:
        params['min_price'] = min_price
        
    max_price = input("Maximum price (leave blank for no maximum): ").strip()
    if max_price:
        params['max_price'] = max_price
    
    # Minimum bids
    min_bids = input("Minimum number of bids (leave blank for no minimum): ").strip()
    if min_bids:
        params['min_bids'] = min_bids
    
    # Sort options
    print("\nSort options:")
    print("1. domain")
    print("2. tldName")
    print("3. endTime")
    print("4. startPrice")
    print("5. currentBid")
    print("6. bids")
    print("7. domainAge")
    print("8. revenue")
    print("9. visitors")
    
    sort_choice = input("Choose sort field (1-9, default: domain): ").strip()
    sort_fields = {
        '1': 'domain', '2': 'tldName', '3': 'endTime',
        '4': 'startPrice', '5': 'currentBid', '6': 'bids',
        '7': 'domainAge', '8': 'revenue', '9': 'visitors'
    }
    if sort_choice in sort_fields:
        params['sortName'] = sort_fields[sort_choice]
    
    sort_dir = input("Sort direction (asc/desc, default: asc): ").strip().lower()
    if sort_dir in ['desc', 'd']:
        params['sortDirection'] = 'descending'
    
    return params

def validate_output(filename):
    """Validate the output CSV file"""
    print("\n" + "=" * 40)
    print("VALIDATING OUTPUT FILE")
    print("=" * 40)
    
    if not os.path.exists(filename):
        print(f"✗ Output file {filename} does not exist")
        return False
        
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        print(f"✓ Output file exists: {filename}")
        print(f"✓ File size: {os.path.getsize(filename):,} bytes")
        print(f"✓ Total lines: {len(lines)}")
        print(f"✓ Data rows: {len(lines) - 1}")  # Subtract header row
        
        # Check header
        header = lines[0].strip()
        expected_headers = ['domain', 'tld', 'time_left', 'starting_price', 'current_bid', 'bids_count', 'domain_age', 'revenue', 'visitors']
        
        if all(col in header for col in expected_headers):
            print("✓ All expected columns are present")
        else:
            print("✗ Some expected columns are missing")
            return False
            
        # Show sample rows
        print("\nSample data from CSV:")
        for i, line in enumerate(lines[1:6]):  # Show first 5 data rows
            print(f"  Row {i+1}: {line.strip()}")
            
        return True
        
    except Exception as e:
        print(f"✗ Error validating output file: {e}")
        return False

def main():
    """Main execution function"""
    print_banner()
    
    # Validate environment
    if not validate_environment():
        sys.exit(1)
    
    # Get search parameters
    search_params = get_search_parameters()
    
    # Ask for page limit
    limit_pages = input("\nLimit number of pages? (enter number or press Enter for all pages): ").strip()
    max_pages = None
    if limit_pages and limit_pages.isdigit():
        max_pages = int(limit_pages)
        print(f"Limiting scraping to {max_pages} pages")
    
    # Initialize components with search parameters
    scraper = PorkbunScraper(max_pages=max_pages, **search_params)
    csv_writer = CSVWriter()
    
    try:
        # Open CSV file
        with csv_writer:
            # Ask user if they want to test first
            print("\nWould you like to run a test first? (recommended)")
            test_choice = input("Enter 'y' for test, 'n' for full scraping: ").lower().strip()
            
            if test_choice == 'y':
                # Run test
                if not test_scraper(scraper, csv_writer):
                    print("✗ Test failed. Please check the errors above.")
                    return
                    
                # Ask if user wants to continue with full scraping
                continue_choice = input("\nTest successful! Continue with full scraping? (y/n): ").lower().strip()
                if continue_choice != 'y':
                    print("Scraping cancelled by user.")
                    return
                    
                # Reset scraper stats for full run (keep same parameters)
                scraper = PorkbunScraper(max_pages=max_pages, **search_params)
            
            # Run full scraping
            if run_full_scraping(scraper, csv_writer, max_pages):
                # Validate output
                validate_output(csv_writer.filename)
                print(f"\n✓ Scraping completed successfully!")
                print(f"✓ Data saved to: {csv_writer.filename}")
            else:
                print("\n✗ Scraping encountered errors")
                
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()