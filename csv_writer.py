import csv
import os
from datetime import datetime
from config import OUTPUT_FILE, CSV_HEADERS

class CSVWriter:
    def __init__(self, filename=None):
        self.filename = filename or OUTPUT_FILE
        self.file = None
        self.writer = None
        self.is_open = False
        
    def __enter__(self):
        self.open()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        
    def open(self):
        """Open the CSV file for writing"""
        try:
            # Check if file exists to determine if we need to write headers
            file_exists = os.path.exists(self.filename) and os.path.getsize(self.filename) > 0
            
            self.file = open(self.filename, 'a', newline='', encoding='utf-8')
            self.writer = csv.writer(self.file)
            
            # Write headers if file is new
            if not file_exists:
                self.writer.writerow(CSV_HEADERS)
                
            self.is_open = True
            print(f"CSV file opened: {self.filename}")
            
        except Exception as e:
            print(f"Error opening CSV file: {e}")
            raise
            
    def close(self):
        """Close the CSV file"""
        if self.file and self.is_open:
            self.file.close()
            self.is_open = False
            print(f"CSV file closed: {self.filename}")
            
    def write_domain_data(self, domain_data):
        """Write a single domain's data to the CSV file"""
        if not self.is_open or not self.writer:
            raise RuntimeError("CSV file is not open. Call open() first.")
            
        try:
            # Ensure all fields are present in the correct order
            row = []
            for header in CSV_HEADERS:
                value = domain_data.get(header, '')
                # Clean up the data
                if isinstance(value, str):
                    value = value.strip()
                row.append(value)
                
            self.writer.writerow(row)
            return True
            
        except Exception as e:
            print(f"Error writing domain data to CSV: {e}")
            return False
            
    def write_multiple_domains(self, domains_data):
        """Write multiple domain records to the CSV file"""
        success_count = 0
        for domain_data in domains_data:
            if self.write_domain_data(domain_data):
                success_count += 1
        return success_count
        
    def get_file_size(self):
        """Get the current size of the CSV file"""
        if os.path.exists(self.filename):
            return os.path.getsize(self.filename)
        return 0
        
    def backup_file(self):
        """Create a backup of the current CSV file"""
        if os.path.exists(self.filename):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{self.filename}.backup_{timestamp}"
            try:
                os.rename(self.filename, backup_filename)
                print(f"Backup created: {backup_filename}")
                return backup_filename
            except Exception as e:
                print(f"Error creating backup: {e}")
        return None