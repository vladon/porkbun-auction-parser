#!/usr/bin/env python3
"""
Test script for Porkbun Auction Parser
Tests the scraper with a small sample of pages without interactive input
"""

from scraper import PorkbunScraper
from csv_writer import CSVWriter

def test_scraper():
    """Test the scraper with a small sample of pages"""
    print("=" * 60)
    print("    Testing Porkbun Auction Parser")
    print("=" * 60)
    
    # Initialize components
    scraper = PorkbunScraper()
    
    try:
        # Open CSV file
        with CSVWriter() as csv_writer:
            print("\nTesting with 2 pages...")
            
            # Test first 2 pages
            test_domains = []
            current_offset = 0
            
            for page in range(2):
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
                if page < 1:
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
            
    except Exception as e:
        print(f"✗ Error during test: {e}")
        return False

if __name__ == "__main__":
    success = test_scraper()
    if success:
        print("\n✓ Test passed! The scraper is working correctly.")
    else:
        print("\n✗ Test failed! Please check the errors above.")