import sys
import json
import os
from datetime import datetime

class ProgressBar:
    """Simple console progress bar for tracking scraping progress"""
    
    def __init__(self, total, width=50, update_interval=10):
        self.total = total
        self.width = width
        self.update_interval = update_interval
        self.current = 0
        self.last_update = 0
        
    def update(self, current, total=None):
        """Update progress bar"""
        if total is not None:
            self.total = total
            
        self.current = current
        
        # Only update at intervals to avoid flickering
        if self.current - self.last_update >= self.update_interval:
            self._draw()
            self.last_update = self.current
            
    def _draw(self):
        """Draw the progress bar"""
        if self.total == 0:
            return
            
        percentage = min(100, (self.current * 100) // self.total)
        filled_width = (self.width * percentage) // 100
        bar = '=' * filled_width + '-' * (self.width - filled_width)
        
        # Calculate ETA
        if self.current > 0 and percentage < 100:
            rate = self.current / (datetime.now().timestamp() - self.start_time) if hasattr(self, 'start_time') else 0
            remaining = self.total - self.current
            eta_seconds = remaining / rate if rate > 0 else 0
            eta = f"ETA: {int(eta_seconds//60)}:{int(eta_seconds%60):02d}" if eta_seconds > 0 else ""
        else:
            eta = ""
            
        sys.stdout.write(f'\r[{bar}] {percentage:3d}% ({self.current}/{self.total}) {eta}')
        sys.stdout.flush()
        
    def start(self):
        """Start timing for ETA calculation"""
        self.start_time = datetime.now().timestamp()
        
    def finish(self):
        """Complete the progress bar"""
        self.update(self.total)
        print()  # New line

class StateManager:
    """Manages saving and loading scraping state for resumption"""
    
    def __init__(self, state_file):
        self.state_file = state_file
        self.state = self._load_state()
        
    def _load_state(self):
        """Load existing state from file"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load state file: {e}")
                return {}
        return {}
        
    def save_state(self, **kwargs):
        """Save current state to file"""
        self.state.update(kwargs)
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save state: {e}")
            
    def get_state(self, key, default=None):
        """Get a specific state value"""
        return self.state.get(key, default)
        
    def clear_state(self):
        """Clear the saved state"""
        self.state = {}
        try:
            if os.path.exists(self.state_file):
                os.remove(self.state_file)
        except OSError as e:
            print(f"Warning: Could not remove state file: {e}")

class AutoFlushWriter:
    """Wrapper for CSV writer with auto-flush capability"""
    
    def __init__(self, csv_writer, flush_interval=100):
        self.csv_writer = csv_writer
        self.flush_interval = flush_interval
        self.domains_written = 0
        
    def write_domain(self, domain_data):
        """Write a single domain and track count"""
        success = self.csv_writer.write_domain(domain_data)
        if success:
            self.domains_written += 1
            
            # Auto-flush at intervals
            if self.domains_written % self.flush_interval == 0:
                self.csv_writer.flush()
                print(f"\n[Auto-flushed] {self.domains_written} domains written to disk")
                
        return success
        
    def write_multiple_domains(self, domains):
        """Write multiple domains and track count"""
        success = self.csv_writer.write_multiple_domains(domains)
        if success:
            self.domains_written += len(domains)
            
            # Auto-flush at intervals
            if self.domains_written % self.flush_interval == 0:
                self.csv_writer.flush()
                print(f"\n[Auto-flushed] {self.domains_written} domains written to disk")
                
        return success
        
    def __getattr__(self, name):
        """Delegate other methods to the wrapped CSV writer"""
        return getattr(self.csv_writer, name)