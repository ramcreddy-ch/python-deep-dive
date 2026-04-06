# 17. Python for Cloud — Boto3, AWS & Infrastructure as Code

> "Cloud is just 'Someone else's computer,' but with an API. An expert doesn't just click in a dashboard; they use Python to automate infrastructure at scale. Mastering Boto3 is the entry ticket to becoming a Cloud, Platform, or SRE engineer."

---

## ❓ The 'Why' (High-Level)
In the modern world, infrastructure is **Volatile**. Nodes spin up and down based on traffic, and data is stored across thousands of globally distributed "Buckets." Doing this manually is impossible. **Boto3** is the official AWS SDK for Python, and it allows you to treat a massive data center as if it were just a Python dictionary. A principal engineer knows that **Automation is the only way to manage 5,000 servers**.

---

## 🌱 Module 1: The Basics (Junior) — The S3 Hello World
Before you start, you must authenticate. AWS uses an **Access Key ID** and a **Secret Access Key**.

### 1. The Survival Kit: Uploading to S3
A "Bucket" is like a folder, and a "Key" is the filename.
```python
import boto3

s3 = boto3.client('s3')
# The junior way: Uploading a file
s3.upload_file("my_cv.pdf", "my-bucket-name", "cv_folder/my_cv.pdf")
```

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — Clients vs. Resources
Mid-level engineers choose the right "Level" of abstraction.

### 1. The "Client" (Low-Level)
- It maps 1:1 with the AWS API. It returns raw JSON dictionaries.
- **When to use**: For everything. Most advanced features only work here.

### 2. The "Resource" (High-Level)
- It provides "Objects" (e.g., `s3.Bucket("name")`).
- **When to use**: For simple scripts where you want cleaner, object-oriented code.

### 3. Enumerating Instances (EC2)
```python
ec2 = boto3.resource('ec2')
for instance in ec2.instances.all():
    print(f"ID: {instance.id}, State: {instance.state['Name']}")
```

---

## 🌳 Module 3: Advanced Mechanics (Senior) — Paginators & Waiters
Senior engineers understand that the cloud is **Asynchronous** and **Massive**.

### 1. Paginators (The Anti-Timeout)
If you have 10,000,000 files in a bucket, the AWS API will only give you 1,000 at a time.
- **The Expert Way**: Use a Paginator to "Scroll" through the list automatically.
```python
paginator = s3.get_paginator('list_objects_v2')
for page in paginator.paginate(Bucket='big-bucket'):
    for obj in page['Contents']: print(obj['Key'])
```

### 2. Waiters
Instead of writing a manual `while True: sleep(1)` loop to check if an instance is ready, use a **Waiter**.
- **Usage**: `s3.get_waiter('bucket_exists').wait(Bucket='my-bucket')`.

---

## 🔥 Module 4: Principal Architect (Principal) — Security & Scale
At the highest level, you manage security boundaries and testability.

### 1. Cross-Account Roles (STS)
A principal engineer never uses long-lived passwords. They use **STS (Security Token Service)** to "Assume" a role temporarily. This is much more secure.

### 2. Mocking the Cloud with `Moto`
You can't run unit tests that cost $0.05 every time you run them.
- **The Expert Way**: Use the **`Moto`** library to "Mockout" AWS. Your tests will think they are talking to AWS, but no network calls are actually made.

---

## 🏗️ Case Study: The "Cloud Janitor"
A startup was spending $100,000 a month on AWS, but 20% of that was "Zombie" resources—unattached storage disks and idle databases.
- **The Junior Approach**: Go through the dashboard and click "Delete" on old things. (Missed 80% of items).
- **The Principal Approach**: Built a Python script using **Boto3** that scanned all 20 AWS Regions, identified anything with a `cost_center` tag missing, and automatically emailed the owner before deleting it 48 hours later.
- **Result**: Cut the AWS bill by **$20,000 per month** in the first scan.

---

## ⚡ Anti-Patterns & Expert Traps

### 1. Hardcoding Credentials
**NEVER** put your AWS Keys in your code. They will eventually end up on GitHub, and an attacker will use your card to mine Bitcoin for $20k in an hour.
- **Expert Fix**: Use **IAM Roles** or Environmental Variables.

### 2. Poor Region Management
AWS is split into regions (us-east-1, eu-west-1). If you don't specify a region, Boto3 might default to one that doesn't have your data, making it look like the bucket is "Missing."

---

## 🎯 Top 20 Principal Interview Questions (Python for Cloud)

1. **Q: What is the difference between a Boto3 'Client' and a 'Resource'?**
   - **Answer**: The **Client** is a low-level, service-wide interface mapping 1:1 with the AWS API. The **Resource** is a high-level, object-oriented abstraction. Clients are generally preferred for production because they support more features.
2. **Q: How does Boto3 find your AWS credentials?**
   - **Answer**: It follows a specific **Credential Provider Chain**: 1. Variables passed directly to the constructor (not recommended). 2. Environment variables. 3. Shared credential file (`~/.aws/credentials`). 4. IAM Role for EC2/Lambda.
3. **Q: What is a 'Paginator' and why is it necessary?**
   - **Answer**: AWS APIs have a limit on how much data they return in one "Page" (e.g., 1,000 objects). A Paginator automatically handles the "NextToken" logic to iterate over millions of items for you.
4. **Q: Explain 'Waiters' in Boto3.**
   - **Answer**: Pre-built objects that poll an AWS service until a resource reaches a specific state (e.g., until an RDS database is 'active'), avoiding the need for manual `while` loops.
5. **Q: What are 'Pre-signed URLs'?**
   - **Answer**: A way to grant **Temporary Access** to a "Private" S3 object. You generate a URL that is valid for a limited time (e.g., 1 hour), allowing someone to download it without needing AWS credentials.
6. **Q: How do you handle 'Throttling' (Rate Limits) in Boto3?**
   - **Answer**: By configuring the **Retry Strategy** in the `Config` object. Boto3 can automatically perform "Exponential Backoff" when it receives a `ProvisionedThroughputExceededException`.
7. **Q: What is the purpose of 'Moto'?**
   - **Answer**: A library used for **Mocking AWS services** in unit tests. It allows you to run your cloud-automation code locally without actually making calls to AWS or incurring costs.
8. **Q: Is Boto3 'Thread-Safe'?**
   - **Answer**: The **Session** object is NOT thread-safe, but the **Client** objects created from a session **ARE** thread-safe. A principal engineer creates a new session per thread but can share a client.
9. **Q: What is 'STS' and how is it used in Python?**
   - **Answer**: Security Token Service. It allows you to "Assume" a cross-account or cross-service **IAM Role** to get temporary, rotating credentials via the `sts_client.assume_role()` call.
10. **Q: How do you perform 'Multipart Upload' for massive files (e.g., 100GB)?**
    - **Answer**: Using the `S3Transfer` manager or the `s3_client.upload_file()` method, which automatically splits the file into pieces and uploads them in parallel.
11. **Q: Explain 'IAM Roles vs IAM Users'.**
    - **Answer**: **Users** have a permanent login/password. **Roles** are meant to be assumed by applications or services temporarily. Roles are significantly more secure for automation scripts.
12. **Q: What is 'Infrastructure as Code' (IaC) and how does Python fit in?**
    - **Answer**: Managing servers/cloud through code rather than clicks. Python is used in IaC tools like **AWS CDK** or for writing "Glue Scripts" between Terraform/CloudFormation stacks.
13. **Q: How do you list all AWS Regions available for a specific service?**
    - **Answer**: By using the `boto3.Session().get_available_regions('service_name')` method.
14. **Q: What is the difference between S3 'Object' and 'Bucket'?**
    - **Answer**: A **Bucket** is the top-level container (like a hard drive). An **Object** is a file stored inside that bucket, identified by a unique **Key**.
15. **Q: Explain 'Tagging' and how to use it in automation.**
    - **Answer**: Tags are Key-Value metadata attached to resources. Automation scripts use them for **Cost Tracking** (e.g., finding all resources tagged with `Project:X`) or **Cleanup**.
16. **Q: How can you check if an S3 bucket already exists before creating it?**
    - **Answer**: Use `s3_client.head_bucket(Bucket='name')`. If it doesn't exist, it will raise a `404` client error.
17. **Q: What is 'BotoCore'?**
    - **Answer**: The low-level foundation library that Boto3 relies on. It handles the raw HTTP requests, retries, and data parsing.
18. **Q: How do you handle 'Region-Specific' S3 buckets?**
    - **Answer**: When creating a bucket, you must specify the `CreateBucketConfiguration` with the `LocationConstraint` matching your desired region.
19. **Q: What is 'Environment Injection' for cloud credentials?**
    - **Answer**: Setting `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` variables in your shell or CI/CD runner so Boto3 picks them up automatically without them being in the code.
20. **Q: What is a 'Dry Run' in Boto3?**
    - **Answer**: Some services (like EC2) allow you to pass `DryRun=True` to a call. AWS will check if you have the right permissions to perform the action without actually doing it.

---

[Previous: DevOps](16-python-devops.md) | [Next: SRE & Observability →](18-python-sre-observability.md)
