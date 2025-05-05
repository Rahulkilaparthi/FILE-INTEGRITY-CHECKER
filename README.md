# File Integrity Checker

A Python tool to monitor changes in files by calculating and comparing hash values. This tool helps ensure file integrity by detecting any modifications, additions, or deletions in a specified directory.

## Features

- Calculate SHA-256 hash values for files
- Establish baseline hashes for a directory
- Monitor files for changes
- Detect new, modified, and deleted files
- Store baseline data in JSON format
- User-friendly command-line interface

## Requirements

- Python 3.6 or higher
- No external dependencies required

## Installation

1. Clone or download this repository

3. Make the script executable:
   ```bash
   chmod +x file_monitor.py
   ```

## Usage

Run the script:
```bash
./file_monitor.py
```

The tool provides three options:

1. **Establish new baseline**: Creates hash values for all files in a specified directory
2. **Verify integrity**: Checks current files against stored baseline hashes
3. **Exit**: Quit the program

### Example Workflow

1. Start the program
2. Choose option 1 to establish a baseline
3. Enter the directory path you want to monitor
4. The tool will create hash values for all files
5. Later, choose option 2 to verify integrity
6. Enter the same directory path
7. The tool will report any changes detected

## How it Works

- Uses SHA-256 hashing algorithm for file integrity checking
- Stores baseline data in a JSON file (`baseline.json`)
- Recursively processes all files in the specified directory
- Detects three types of changes:
  - New files added
  - Existing files modified
  - Files deleted

## Security Considerations

- The tool uses cryptographic hash functions (SHA-256) for reliable file integrity checking
- Baseline data is stored locally and can be backed up
- The tool does not modify any monitored files 
