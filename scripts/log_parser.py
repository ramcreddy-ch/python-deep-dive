import re
import sys
import argparse
from collections import Counter

def analyze_logs(log_path, pattern=r'ERROR'):
    """
    Production log parser for large files.
    Demonstrates: Regex, Large-file processing, and CLI arguments.
    """
    matcher = re.compile(pattern)
    record_counts = Counter()

    try:
        with open(log_path, 'r') as f:
            for line in f:
                if matcher.search(line):
                    # Basic extraction logic
                    parts = line.split()
                    if len(parts) > 2:
                        service = parts[2]
                        record_counts[service] += 1
                        
        print(f"\n--- Production Log Analysis (Pattern: {pattern}) ---")
        for service, count in record_counts.most_common(10):
            print(f"{service}: {count} occurrences")
            
    except FileNotFoundError:
        print(f"Error: File {log_path} not found.")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Professional Log Analyzer")
    parser.add_argument("file", help="Path to the log file")
    parser.add_argument("--pattern", default="ERROR", help="Regex pattern to search for")
    
    args = parser.parse_args()
    analyze_logs(args.file, args.pattern)
