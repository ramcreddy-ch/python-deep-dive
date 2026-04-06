import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upload_to_s3(local_file, bucket, s3_file=None):
    """
    Uploads a file to an S3 bucket.
    Demonstrates: Boto3, Error Handling, and Pathlib.
    """
    s3 = boto3.client('s3')

    if s3_file is None:
        s3_file = Path(local_file).name

    try:
        logger.info(f"Uploading {local_file} to {bucket}/{s3_file}...")
        s3.upload_file(local_file, bucket, s3_file)
        logger.info("Upload Successful")
        return True
    except FileNotFoundError:
        logger.error("The file was not found")
        return False
    except NoCredentialsError:
        logger.error("Credentials not available")
        return False
    except PartialCredentialsError:
        logger.error("Incomplete credentials")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    # Note: This requires AWS credentials configured (e.g., via ~/.aws/credentials or env vars)
    # create_dummy_file
    dummy_file = "payload.txt"
    Path(dummy_file).write_text("Hello Cloud!")
    
    # upload_to_s3(dummy_file, "my-production-bucket")
    print("Example ready. Run with valid AWS credentials and bucket name.")
