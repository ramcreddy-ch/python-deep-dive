# 10. Python for Cloud — AWS, Azure, GCP Deep Dive

> Boto3 (AWS) is downloaded over 300 million times a month. But simply knowing how to initialize a client isn't enough. Production cloud engineering requires strict credential management, efficient pagination, retry policies, and session architectures.

---

## ☁️ AWS (Boto3) Architecture

### Clients vs. Resources
Boto3 offers two interfaces. 
*   **Clients:** Low-level, 1-to-1 mapping with the raw AWS API. Returns massive JSON dictionaries.
*   **Resources:** (Deprecated in some newer APIs, heavily used in older scripts). High-level, object-oriented, Pythonic mappings. Returns Python objects.

*Modern best practice dictates using **Clients** for everything to ensure maximum API feature coverage and performance.*

### The Pagination Problem
If you query AWS for a list of S3 objects or EC2 instances, it defaults to returning a maximum of 1,000 items. If you don't implement pagination, your script silently ignores 90% of your infrastructure.

```python
import boto3

# BAD (Silently fails at 1000 items)
s3 = boto3.client('s3')
res = s3.list_objects_v2(Bucket='ml-massive-data')
for obj in res.get('Contents', []):
    print(obj['Key'])

# GOOD (The Production Paginator Pattern)
s3 = boto3.client('s3')
paginator = s3.get_paginator('list_objects_v2')

# Automates the "NextContinuationToken" loop natively
page_iterator = paginator.paginate(Bucket='ml-massive-data')
for page in page_iterator:
    for obj in page.get('Contents', []):
        print(obj['Key'])
```

---

## 🏭 Security & Auth (The Boto3 Default Chain)

Never hardcode `aws_access_key_id`. Boto3 uses a standard credential resolution chain. When running in a K8s pod or EC2 instance, you assign an IAM Role to the compute primitive. Boto3 will automatically query the metadata service (IMDSv2) at `169.254.169.254` to retrieve temporary, rotating credentials.

```python
import boto3

# This is all you need. Boto3 automatically figures out how to authenticate 
# whether running on your laptop (~/.aws/credentials) or in the cloud (IAM Role).
ec2_client = boto3.client('ec2', region_name='us-west-2')
```

### Assuming Roles (Cross-Account Architecture)
Enterprise clouds use Hub-and-Spoke accounts. You compute in `Account A` but need to manipulate S3 in `Account B`. You must execute an STS AssumeRole.

```python
import boto3

sts = boto3.client('sts')
credentials = sts.assume_role(
    RoleArn="arn:aws:iam::123456789012:role/CrossAccountSRE",
    RoleSessionName="PythonSRESession"
)['Credentials']

# Inject the temporary credentials to create a new authenticated client
s3_xaccount = boto3.client(
    's3',
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken']
)
```

---

## ⚡ Cloud Functions / Serverless (Lambda Serverless)

When writing Python for AWS Lambda or GCP Cloud functions, understand the **Cold Start** vs **Warm Start** execution environment.

```python
import json
import boto3

# WARM START ZONE (Executed once during container boot)
# Initialize heavy resources OUTSIDE the handler handler
# so they are cached across invocations.
dynamodb = boto3.client('dynamodb')
MODEL_WEIGHTS = load_model_from_disk()

def lambda_handler(event, context):
    # COLD START ZONE (Executed on every single API request)
    # Fast, stateless operations only.
    record_id = event['pathParameters']['id']
    
    res = dynamodb.get_item(TableName="Users", Key={"id": {"S": record_id}})
    return {
        "statusCode": 200,
        "body": json.dumps(res.get("Item"))
    }
```

---

## 🎯 Senior Engineer Interview Questions

**Q1: We deployed a Python script inside an AWS EKS Cluster. The pods are randomly experiencing `botocore.exceptions.ClientError: TooManyRequestsException`. How do we solve this?**
> **Answer:** Boto3 has a default retry mechanism, but under high concurrency (e.g., pulling config for 500 pods), AWS APIs rigidly throttle requests. You must configure the Boto3 `Config` object to modify the retry behavior.
> ```python
> from botocore.config import Config
> custom_config = Config(
>     retries={"max_attempts": 10, "mode": "adaptive"} # 'adaptive' auto-paces API calls
> )
> s3 = boto3.client("s3", config=custom_config)
> ```

**Q2: Explain how you would safely stream a 50GB file from AWS S3 directly into a Python memory buffer without running out of RAM.**
> **Answer:** We can't use `s3.get_object()['Body'].read()` as it will load all 50GB into memory. I would use the `s3.download_fileobj()` method wrapped around an an in-memory stream, or more simply, stream chunks manually using the `StreamingBody.read(chunk_size)` iterator. Better yet, if parsing CSV/Parquet, I'd use `awswrangler` (AWS SDK for Pandas) which abstracts optimized, chunked S3 streaming.

**Q3: Describe how authentication works in GCP using Python.**
> **Answer:** GCP uses Application Default Credentials (ADC). The Python Google Cloud libraries (`google-cloud-storage`, etc.) look for the `GOOGLE_APPLICATION_CREDENTIALS` environment variable pointing to a service account JSON file. If not running locally, and executing inside a GCP compute instance (GKE/Compute Engine), the library securely queries the GCP metadata server to obtain temporary, rolling OAuth 2.0 access tokens linked to the instance's Service Account.

**Q4: You have a Lambda function doing heavy text processing. It runs out of time after 15 minutes. How do you scale this architecture?**
> **Answer:** Lambda has a hard cap of 15 minutes. If a single payload requires more processing time, the monolith architecture must be decoupled. I would use AWS Step Functions to coordinate a distributed Map-Reduce pattern, fanning out the workloads to dozens of parallel Lambda invocations. If a single task is inherently monolithic and cannot be parallelized, I would move the execution from Lambda to AWS Fargate (ECS) or AWS Batch, which have no execution time limits.

---

[← Previous: Python for DevOps](09-python-devops.md) | [Back to Index](../README.md) | [Next: Python for SRE →](11-python-sre.md)
