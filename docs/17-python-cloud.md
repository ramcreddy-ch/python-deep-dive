# 17. Python for Cloud — AWS, Boto3 & Infrastructure Management

> "Cloud isn't just someone else's computer; it's a giant, programmable API. Expert Cloud Engineers use Python to treat AWS, Azure, and GCP as living codebases — automating resource lifecycles, auditing security, and scaling infrastructure with precision."

---

## 🌱 The Basics: Boto3 & Configuration
The entry-level way to talk to AWS using **Boto3**.

```python
import boto3

# 1. Create a client for S3
s3 = boto3.client("s3")

# 2. List all buckets
# response = s3.list_buckets()
# for bucket in response['Buckets']:
#     print(f"Bucket: {bucket['Name']}")
```

---

## 🌿 Intermediate: Clients vs. Resources
Boto3 provides two ways to interact with AWS:
- **Client**: Low-level, direct mapping to the AWS API. Returns raw JSON. Best for speed and advanced features.
- **Resource**: High-level, object-oriented abstraction. Much easier to read and write.

```python
# 1. Low-level Client (JSON-based)
s3_client = boto3.client("s3")
s3_client.upload_file("test.txt", "my-bucket", "test.txt")

# 2. High-level Resource (Object-based)
s3_resource = boto3.resource("s3")
bucket = s3_resource.Bucket("my-bucket")
# bucket.upload_file("test.txt", "test.txt")
```

---

## 🌳 Advanced: IAM & Security (The Credential Chain)
Senior engineers never hardcode AWS keys. Boto3 automatically looks for credentials in this order:
1.  **Params**: Passed directly to `boto3.client()`. (Avoid in prod!)
2.  **EnvVars**: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`.
3.  **Config**: The `~/.aws/credentials` file.
4.  **IAM Role**: If running on an EC2 instance or as a Lambda, it uses the **Instance Profile** automatically.

**Real Use (Compliance/Security)**:
A script that audits all S3 buckets for public access and "Locks" them.

```python
def lock_s3_buckets():
    """
    Expert Pattern: Security Guardrail. 
    Demonstrates: Automating compliance via Cloud APIs.
    """
    s3 = boto3.client("s3")
    # bucket_list = s3.list_buckets()['Buckets']
    # for b in bucket_list:
    #     s3.put_public_access_block(...)
```

---

## 🔥 Expert: Paginators & Waiters
Principal engineers understand that the Cloud API is **Throttled** and **Paginated**.

### 1. Paginators
If you have 10,000 files in S3, `list_objects` only returns the first 1,000. You **must** use a Paginator to see everything.

### 2. Waiters
Instead of writing a `while True` loop to check if an EC2 instance is "Running", use a Waiter. It's an optimized, high-performance polling system built into Boto3.

---

## 🎯 Top 20 Principal Interview Questions (Cloud Engineering)

1. **Q: What is Boto3?**
   - **Answer**: It is the official AWS SDK for Python, allowing you to programmatically manage almost every AWS service (EC2, S3, IAM, etc.) via its API.
2. **Q: Explain the difference between Boto3 Client and Resource.**
   - **Answer**: A **Client** is low-level, returning raw JSON dictionaries. It maps 1:1 to the AWS API. A **Resource** is high-level, returning Python objects with attributes/methods. Not all AWS services support the Resource interface.
3. **Q: How does Boto3 find your AWS credentials in production?**
   - **Answer**: It follows the **Credential Provider Chain**, looking first at environment variables, then local configuration files, and finally at the **IAM Instance Profile** attached to the EC2/Lambda environment.
4. **Q: What is a 'Paginator' and why is it mandatory for large datasets?**
   - **Answer**: Most AWS APIs truncate results to 1,000 items. A **Paginator** automatically handles the 'NextToken' or 'Marker' logic to iterate through all results in the cloud without missing any.
5. **Q: What is a 'Waiter' in Boto3?**
   - **Answer**: It is a tool that "Polls" an AWS resource until it reaches a desired state (e.g., waiting for an EC2 instance to go from 'Pending' to 'Running'). It is more efficient than manual sleep loops.
6. **Q: How do you handle 'API Rate Limiting' (Throttling) in Boto3?**
   - **Answer**: Boto3 has built-in **Retries with Exponential Backoff**. You can customize this by passing a `Config` object to the client with `max_attempts` set.
7. **Q: Why should you avoid hardcoding AWS Access Keys in your script?**
   - **Answer**: It is a major security risk. If the code is leaked (e.g., committed to GitHub), an attacker can use those keys to delete your infrastructure or steal data. Use **IAM Roles** instead.
8. **Q: How do you connect to an AWS service in a specific 'Region'?**
   - **Answer**: Pass the `region_name` parameter to the client: `boto3.client("ec2", region_name="us-west-2")`.
9. **Q: What is 'Infrastructure as Code' (IaC) and how does Python fit into it?**
   - **Answer**: managing infrastructure via code files. Python is used in tools like **Pulumi** and **AWS CDK** (Cloud Development Kit) to define resources using real Python logic instead of just YAML.
10. **Q: What is a 'Multipart Upload' in S3?**
    - **Answer**: A process of breaking a very large file (e.g., 50GB) into smaller chunks and uploading them simultaneously. Boto3's `S3Transfer` manager handles this automatically.
11. **Q: How do you update a 'Security Group' rule using Python?**
    - **Answer**: Using the EC2 client's `authorize_security_group_ingress()` method to add an IP address or port to the allowed list.
12. **Q: What is the purpose of `boto3.Session()`?**
    - **Answer**: It allows you to manage multiple AWS profiles and sets of credentials in the same script. If you don't use it, Boto3 uses the "Default" session.
13. **Q: How do you handle 'Idempotency' when creating an EC2 instance?**
    - **Answer**: Use the `ClientToken` parameter. If you send the same token twice, AWS will detect it's a duplicate and won't create a second instance.
14. **Q: What is 'Serverless' and how does Python run on AWS Lambda?**
    - **Answer**: Serverless means you don't manage the underlying server. Python on Lambda requires a "Handler" function that AWS calls when an event (like an HTTP request or a file upload) occurs.
15. **Q: How do you manage Python dependencies in an AWS Lambda function?**
    - **Answer**: By creating a **Lambda Layer** containing your `site-packages` or by bundling all dependencies into a **Zip Deployment Package** or a **Docker Image**.
16. **Q: What is the difference between S3 'Bucket Policy' and 'ACL'?**
    - **Answer**: A **Bucket Policy** is a JSON document that manages access to the entire bucket or folders. **ACLs** are an older method for managing access on a per-file (Object) basis.
17. **Q: How can you find all EBS volumes that are "Available" (not attached) to save costs?**
    - **Answer**: Iterating through `ec2.volumes.filter(Filters=[{'Name': 'status', 'Values': ['available']}])`.
18. **Q: What is 'Presigned URL' in S3?**
    - **Answer**: A temporary URL generated via Python that allows a user to download or upload a specific file for a limited time (e.g., 10 minutes) without having AWS credentials.
19. **Q: How do you use Python to monitor CloudWatch Logs?**
    - **Answer**: Using the `logs` client's `filter_log_events()` method to search for specific strings (like "ERROR") across log groups.
20. **Q: What is the benefit of the 'AWS CDK' over raw Boto3 scripts?**
    - **Answer**: The CDK allows you to define complex, multi-resource architectures (like a VPC + RDS + Load Balancer) as stable, versioned **Stacks** that can be deployed and destroyed as a single unit.

---

[← Previous: DevOps](16-python-devops.md) | [Next: SRE →](18-python-sre.md)
