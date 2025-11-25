#!/usr/bin/env python3
"""
Run full scraping of Porkbun auction pages with multithreading
"""

import sys
import os
from datetime import datetime
from scraper_mt import PorkbunScraper
from csv_writer import CSVWriter
from config import SEARCH_PARAMS

def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("    Porkbun Auction Parser - Multithreaded Edition")
    print("    Scraping all domain auction data from porkbun.com")
    print("=" * 60)
    print()

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
    
    # Initialize components with multithreading and search parameters
    scraper = PorkbunScraper(max_workers=10, max_pages=max_pages, **search_params)
    csv_writer = CSVWriter()
    
    try:
        # Open CSV file
        with csv_writer:
            print("Starting full scraping with multithreading...")
            print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Scrape all pages
            all_domains, total_domains = scraper.scrape_all_pages(max_workers=10)
            
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

if __name__ == "__main__":
    success = main()
    if success:
        print(f"\n✓ Multithreaded scraping completed successfully!")
        print(f"✓ Data saved to: {csv_writer.filename}")
    else:
        print("\n✗ Scraping encountered errors")
        sys.exit(1)