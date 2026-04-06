import json
import logging
from collections import Counter
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def parse_logs(log_file_path):
    """
    Parses a structured JSON log file and calculates metrics.
    Demonstrates: File I/O, JSON, Collections, and Logging.
    """
    path = Path(log_file_path)
    if not path.exists():
        logger.error(f"Log file {log_file_path} not found.")
        return

    status_counts = Counter()
    errors = []

    with path.open('r') as f:
        for line_num, line in enumerate(f, 1):
            try:
                entry = json.loads(line)
                status = entry.get('status')
                if status:
                    status_counts[status] += 1
                
                if status == 'ERROR':
                    errors.append({
                        'line': line_num,
                        'message': entry.get('message', 'No message'),
                        'timestamp': entry.get('timestamp')
                    })
            except json.JSONDecodeError:
                logger.warning(f"Skipping malformed JSON at line {line_num}")

    # Output Results
    print("\n--- Log Metrics Summary ---")
    print(f"Total entries processed: {sum(status_counts.values())}")
    for status, count in status_counts.items():
        print(f"[{status}]: {count}")

    if errors:
        print("\n--- Recent Errors ---")
        for err in errors[-5:]: # Show last 5
            print(f"Line {err['line']} | {err['timestamp']} | {err['message']}")

if __name__ == "__main__":
    # Create a dummy log file for demonstration
    dummy_log = "app.log"
    with open(dummy_log, "w") as f:
        f.write(json.dumps({"timestamp": "2024-05-18T12:00:01", "status": "INFO", "message": "App started"}) + "\n")
        f.write(json.dumps({"timestamp": "2024-05-18T12:00:05", "status": "ERROR", "message": "Database connection failed"}) + "\n")
        f.write(json.dumps({"timestamp": "2024-05-18T12:00:10", "status": "INFO", "message": "User logged in", "user_id": 42}) + "\n")
        f.write(json.dumps({"timestamp": "2024-05-18T12:00:15", "status": "ERROR", "message": "Disk pressure detected"}) + "\n")

    parse_logs(dummy_log)
