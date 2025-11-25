import requests
import time
import random
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config import (
    BASE_URL, HEADERS, REQUEST_DELAY_MIN, REQUEST_DELAY_MAX,
    MAX_RETRIES, RETRY_DELAY, DOMAINS_PER_PAGE, MAX_PAGES_TO_PROCESS
)

class PorkbunScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.total_domains_scraped = 0
        self.total_pages_scraped = 0
        self.error_count = 0
        
    def _make_request(self, url, retry_count=0):
        """Make HTTP request with retry logic"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response
            
        except requests.exceptions.RequestException as e:
            if retry_count < MAX_RETRIES:
                print(f"Request failed (attempt {retry_count + 1}/{MAX_RETRIES}): {e}")
                print(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
                return self._make_request(url, retry_count + 1)
            else:
                print(f"Request failed after {MAX_RETRIES} attempts: {e}")
                self.error_count += 1
                return None
                
    def _extract_domain_data_from_row(self, row):
        """Extract domain data from a table row"""
        try:
            cells = row.find_all('td')
            if len(cells) < 10:  # We expect at least 10 columns
                return None
                
            # Extract data from each cell in correct order
            # Based on the table structure: Domain, TLD, Time Left, Starting Price, Current Bid, Bids, Domain Age, Revenue, Visitors
            domain_cell = cells[0].find('a')
            domain = domain_cell.text.strip() if domain_cell else cells[0].text.strip()
            
            # Extract TLD from the TLD column (2nd column)
            tld = cells[1].text.strip()
            
            time_left = cells[2].text.strip()  # Time Left is 3rd column
            starting_price = cells[3].text.strip()  # Starting Price is 4th column
            current_bid = cells[4].text.strip()  # Current Bid is 5th column
            bids_count = cells[5].text.strip()  # Bids is 6th column
            domain_age = cells[6].text.strip()  # Domain Age is 7th column
            revenue = cells[7].text.strip()  # Revenue is 8th column
            visitors = cells[8].text.strip()  # Visitors is 9th column
            
            # Clean up the data
            return {
                'domain': domain,
                'tld': tld,
                'time_left': time_left,
                'starting_price': starting_price,
                'current_bid': current_bid,
                'bids_count': bids_count,
                'domain_age': domain_age,
                'revenue': revenue,
                'visitors': visitors
            }
            
        except Exception as e:
            print(f"Error extracting data from row: {e}")
            return None
            
    def _extract_domains_from_page(self, soup):
        """Extract all domain data from a page"""
        domains = []
        
        try:
            # Find the main table containing domain data
            table = soup.find('table')
            if not table:
                print("No table found on the page")
                return domains
                
            # Find all rows in the table body
            rows = table.find_all('tr')
            
            for row in rows:
                # Skip header row and rows without enough cells
                if row.find('th') or len(row.find_all('td')) < 9:
                    continue
                    
                domain_data = self._extract_domain_data_from_row(row)
                if domain_data:
                    domains.append(domain_data)
                    
        except Exception as e:
            print(f"Error extracting domains from page: {e}")
            
        return domains
        
    def _get_total_domains_count(self, soup):
        """Extract the total number of domains from the page"""
        try:
            # Look for text like "Showing 1 - 100 out of 286308 results"
            text_elements = soup.find_all(text=re.compile(r'Showing.*out of.*results'))
            for text in text_elements:
                match = re.search(r'out of (\d+)', text)
                if match:
                    return int(match.group(1))
        except Exception as e:
            print(f"Error extracting total domains count: {e}")
        return None
        
    def _rate_limit_delay(self):
        """Implement rate limiting with random delay"""
        delay = random.uniform(REQUEST_DELAY_MIN, REQUEST_DELAY_MAX)
        time.sleep(delay)
        return delay
        
    def scrape_page(self, offset=0):
        """Scrape a single page of auction results"""
        url = f"{BASE_URL}?from={offset}" if offset > 0 else BASE_URL
        
        print(f"Scraping page: {url}")
        
        # Make the request
        response = self._make_request(url)
        if not response:
            return None, 0
            
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract domain data
        domains = self._extract_domains_from_page(soup)
        
        # Get total domains count (only on first page)
        total_domains = None
        if offset == 0:
            total_domains = self._get_total_domains_count(soup)
            if total_domains:
                print(f"Total domains found: {total_domains}")
                
        # Update counters
        self.total_pages_scraped += 1
        self.total_domains_scraped += len(domains)
        
        return domains, total_domains
        
    def scrape_all_pages(self, max_pages=None):
        """Scrape all auction pages"""
        if max_pages is None:
            max_pages = MAX_PAGES_TO_PROCESS
            
        all_domains = []
        total_domains = None
        current_offset = 0
        page_count = 0
        
        print("Starting to scrape Porkbun auction pages...")
        
        while page_count < max_pages:
            # Scrape current page
            domains, total_count = self.scrape_page(current_offset)
            
            if domains is None:
                print("Failed to scrape page. Stopping.")
                break
                
            if not domains:
                print("No more domains found. Stopping.")
                break
                
            all_domains.extend(domains)
            page_count += 1
            
            # Set total domains count from first page
            if total_count is not None:
                total_domains = total_count
                estimated_pages = (total_domains + DOMAINS_PER_PAGE - 1) // DOMAINS_PER_PAGE
                print(f"Estimated total pages to scrape: {estimated_pages}")
                
            # Progress update
            print(f"Page {page_count} completed: {len(domains)} domains scraped")
            print(f"Total domains scraped so far: {self.total_domains_scraped}")
            
            # Check if we've scraped all domains
            if total_domains and self.total_domains_scraped >= total_domains:
                print("All domains have been scraped.")
                break
                
            # Move to next page
            current_offset += DOMAINS_PER_PAGE
            
            # Rate limiting
            if page_count < max_pages:  # Don't delay after the last page
                delay = self._rate_limit_delay()
                print(f"Waiting {delay:.2f} seconds before next request...")
                
        print(f"\nScraping completed!")
        print(f"Total pages scraped: {page_count}")
        print(f"Total domains scraped: {self.total_domains_scraped}")
        print(f"Total errors encountered: {self.error_count}")
        
        return all_domains, total_domains
        
    def get_scraping_stats(self):
        """Get current scraping statistics"""
        return {
            'total_domains_scraped': self.total_domains_scraped,
            'total_pages_scraped': self.total_pages_scraped,
            'error_count': self.error_count
        }