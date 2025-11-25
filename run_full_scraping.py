#!/usr/bin/env python3
"""
Full scraping script for Porkbun Auction Parser
Runs the complete scraping process for all auction pages
"""

from scraper import PorkbunScraper
from csv_writer import CSVWriter
import os

def run_full_scraping():
    """Run the full scraping process for all pages"""
    print("=" * 60)
    print("    Running Full Porkbun Auction Scraping")
    print("=" * 60)
    
    # Initialize components
    scraper = PorkbunScraper()
    
    # Check if CSV file already exists
    csv_filename = "porkbun_auctions.csv"
    if os.path.exists(csv_filename):
        print(f"⚠ CSV file {csv_filename} already exists.")
        print("Data will be appended to existing file.")
        
        # Show current file size
        file_size = os.path.getsize(csv_filename)
        print(f"Current file size: {file_size:,} bytes")
    
    try:
        # Open CSV file
        with CSVWriter() as csv_writer:
            print("\nStarting full scraping process...")
            print("This will take several hours due to rate limiting.")
            print("Press Ctrl+C to stop at any time.")
            print()
            
            # Scrape all pages
            all_domains, total_domains = scraper.scrape_all_pages()
            
            if all_domains:
                # Write all data to CSV
                success_count = csv_writer.write_multiple_domains(all_domains)
                print(f"\n✓ Successfully wrote {success_count} domains to CSV")
                
                # Show final statistics
                stats = scraper.get_scraping_stats()
                print(f"\nFinal Statistics:")
                print(f"  Total domains scraped: {stats['total_domains_scraped']}")
                print(f"  Total pages scraped: {stats['total_pages_scraped']}")
                print(f"  Total errors: {stats['error_count']}")
                
                if total_domains:
                    completion_rate = (stats['total_domains_scraped'] / total_domains) * 100
                    print(f"  Completion rate: {completion_rate:.2f}%")
                    
                # Validate output file
                final_file_size = os.path.getsize(csv_filename)
                print(f"\nOutput file: {csv_filename}")
                print(f"Final file size: {final_file_size:,} bytes")
                print(f"File size increase: {final_file_size - file_size:,} bytes" if 'file_size' in locals() else f"Final file size: {final_file_size:,} bytes")
                
                return True
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

if __name__ == "__main__":
    success = run_full_scraping()
    if success:
        print("\n✓ Scraping completed successfully!")
        print("You can now analyze the data in porkbun_auctions.csv")
    else:
        print("\n✗ Scraping encountered errors or was interrupted")