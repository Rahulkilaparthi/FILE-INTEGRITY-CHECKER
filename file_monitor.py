#!/usr/bin/env python3

import hashlib
import json
import os
import time
from datetime import datetime
from typing import Dict, Optional

class FileIntegrityChecker:
    def __init__(self, baseline_file: str = "baseline.json"):
        """
        Initialize the File Integrity Checker
        
        Args:
            baseline_file (str): Path to store the baseline hashes
        """
        self.baseline_file = baseline_file
        self.baseline_hashes = self._load_baseline()

    def calculate_file_hash(self, filepath: str) -> Optional[str]:
        """
        Calculate SHA-256 hash of a file
        
        Args:
            filepath (str): Path to the file
            
        Returns:
            str: Hash value of the file or None if file doesn't exist
        """
        if not os.path.exists(filepath):
            return None
            
        sha256_hash = hashlib.sha256()
        
        try:
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            print(f"Error calculating hash for {filepath}: {e}")
            return None

    def _load_baseline(self) -> Dict:
        """Load baseline hashes from file if it exists"""
        if os.path.exists(self.baseline_file):
            try:
                with open(self.baseline_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading baseline file: {e}")
        return {}

    def save_baseline(self):
        """Save current baseline hashes to file"""
        with open(self.baseline_file, 'w') as f:
            json.dump(self.baseline_hashes, f, indent=4)

    def establish_baseline(self, directory: str):
        """
        Create baseline hashes for all files in specified directory
        
        Args:
            directory (str): Directory to monitor
        """
        for root, _, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_hash = self.calculate_file_hash(filepath)
                if file_hash:
                    self.baseline_hashes[filepath] = {
                        'hash': file_hash,
                        'last_modified': os.path.getmtime(filepath),
                        'timestamp': datetime.now().isoformat()
                    }
        self.save_baseline()
        print(f"Baseline established for {len(self.baseline_hashes)} files")

    def verify_integrity(self, directory: str) -> bool:
        """
        Check if any files have been modified since baseline
        
        Args:
            directory (str): Directory to check
            
        Returns:
            bool: True if all files match baseline, False otherwise
        """
        all_files_match = True
        current_files = set()

        # Check existing files
        for root, _, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                current_files.add(filepath)
                
                current_hash = self.calculate_file_hash(filepath)
                baseline_data = self.baseline_hashes.get(filepath)

                if not baseline_data:
                    print(f"New file detected: {filepath}")
                    all_files_match = False
                elif current_hash != baseline_data['hash']:
                    print(f"File modified: {filepath}")
                    print(f"Original hash: {baseline_data['hash']}")
                    print(f"Current hash: {current_hash}")
                    all_files_match = False

        # Check for deleted files
        baseline_files = set(self.baseline_hashes.keys())
        deleted_files = baseline_files - current_files
        if deleted_files:
            all_files_match = False
            for filepath in deleted_files:
                print(f"File deleted: {filepath}")

        return all_files_match

def main():
    """Main function to demonstrate usage"""
    checker = FileIntegrityChecker()
    
    while True:
        print("\nFile Integrity Checker Menu:")
        print("1. Establish new baseline")
        print("2. Verify integrity")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            directory = input("Enter directory path to monitor: ")
            if os.path.exists(directory):
                checker.establish_baseline(directory)
            else:
                print("Invalid directory path!")
                
        elif choice == "2":
            directory = input("Enter directory path to check: ")
            if os.path.exists(directory):
                if checker.verify_integrity(directory):
                    print("All files match baseline!")
                else:
                    print("Changes detected! See above for details.")
            else:
                print("Invalid directory path!")
                
        elif choice == "3":
            print("Exiting...")
            break
            
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main() 