# 25. Advanced Security — Injection, RCE & Supply Chain Hardening

> "In the cloud, security isn't a feature; it's a prerequisite. An expert doesn't just 'use' libraries; they audit them. They know how to prevent code execution attacks and how to secure Python applications against malicious actors."

---

## 🌱 The Basics: Input Sanitization
The entry-level way to keep your app safe is to never trust user input.

- **Injection**: An attacker sends a string like `1; rm -rf /`. If your code runs it, he has deleted your file system.
- **Solution**: Always use **Parameterized Inputs** (like in SQL or Subprocess) that treat user text as a "String", not as "Code".

```python
import subprocess

# 1. DANGER: User can inject a command like '; rm -rf'
def unsafe_ping(host):
    # This runs a code through a Shell (Dangerous!)
    subprocess.run(f"ping {host}", shell=True)

# 2. SECURE: Passed as a list (Safe!)
def secure_ping(host):
    # This treats everything as a String, not Code.
    subprocess.run(["ping", "-c", "1", host])
```

---

## 🌿 Intermediate: Snyk & Dependency Auditing
`Snyk` or `pip-audit` are tools that scan your `requirements.txt` for libraries with known security bugs (CVEs).

**Real Use (DevSecOps)**:
Failing a CI/CD build if a security vulnerability is found in one of your packages.

```bash
# Professional Auditing: Run in your pipeline
pip-audit
```

---

## 🌳 Advanced: RCE & Insecure Deserialization
Senior engineers avoid **Pickle** for public APIs because it is vulnerable to **Remote Code Execution (RCE)**. An attacker can create a special "Model" file that, when you load it, sends all your database passwords to the attacker's server.

**The Fix**: Use **JSON** or **MessagePack** for untrusted data.

```python
import json

# Safe Data Loading
def load_api_data(data_string):
    """
    Expert Pattern: Data Isolation. 
    Demonstrates: Loading JSON instead of Pickle.
    """
    return json.loads(data_string)
```

---

## 🔥 Expert: Vault Integration & Secret Masking
Principal engineers use **HashiCorp Vault** or **AWS Secrets Manager** to manage keys. They also write custom logging filters to "Mask" secrets in the logs.

```python
import logging

class SecretFilter(logging.Filter):
    """
    Principal Pattern: Log Sanitization. 
    Demonstrates: Preventing API keys from leaking into production logs.
    """
    def filter(self, record):
        # Logic to find and mask anything that looks like an API key
        if "sk-" in record.msg:
            record.msg = record.msg.replace("sk-", "MASKED-")
        return True

# logger = logging.getLogger("APP")
# logger.addFilter(SecretFilter())
```

---

## 🎯 Top 20 Principal Interview Questions (Advanced Security)

1. **Q: What is 'Command Injection' and how do you prevent it?**
   - **Answer**: It's an attack where a user inputs OS commands (like `; rm -rf /`) into a script. Prevent it by using **List-based arguments** in `subprocess.run()` instead of `shell=True`.
2. **Q: Why is `eval()` considered extremely dangerous?**
   - **Answer**: `eval()` executes **any** string as Python code. If it's used on user input, it gives the user full control over your server (Remote Code Execution).
3. **Q: Explain 'Insecure Deserialization' (Pickle).**
   - **Answer**: `pickle.load()` can execute arbitrary code stored in the file. An attacker can create a malicious pickle file that grants them access to your system. Never unpickle data from untrusted sources.
4. **Q: What is a 'Denial of Service' (DoS) in Python?**
   - **Answer**: An attack that slows down or crashes a server (e.g., by sending a massive JSON file or a complex Regex that causes a ReDoS).
5. **Q: How do you prevent 'SQL Injection' in Python?**
   - **Answer**: **Always** use parameterized queries (e.g., `cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))`). Never use f-strings or manual string concatenation to build a query.
6. **Q: What is 'Secrets Management'?**
   - **Answer**: The practice of storing sensitive keys and passwords in a **secure Vault** (like AWS Secrets Manager or HashiCorp Vault) rather than hardcoding them in code or `.env` files.
7. **Q: Explain 'Supply Chain Hardening' in Python.**
   - **Answer**: This involves verifying that the libraries you use are safe: **Auditing** dependencies for CVEs, pinning **Exact Versions** (hashes), and ignoring untrusted repositories.
8. **Q: What is 'ReDoS' (Regular Expression Denial of Service)?**
   - **Answer**: A vulnerability where a malicious string is sent to a complex regex, causing the engine to "backtrack" endlessly and consume 100% of the CPU.
9. **Q: What is a 'Timing Attack' and how can Python be vulnerable?**
   - **Answer**: An attack where an attacker can figure out a secret (like a password) by measuring how long a function takes to execute. In Python, use `secrets.compare_digest()` for safe comparisons.
10. **Q: What is the purpose of the `secrets` module?**
    - **Answer**: To generate **cryptographically strong** random numbers for passwords, secrets, and security tokens. Standard `random` is predictable and NOT safe for security.
11. **Q: Explain 'JWT' (JSON Web Token) security concerns.**
    - **Answer**: Ensure tokens are **Signed** (using a secret) and preferably **Encrypted**. Always check the expiration (`exp`) and the signature before trusting the token.
12. **Q: What is 'Hashing' and why do we never store passwords in 'Plain Text'?**
    - **Answer**: Hashing is a one-way mathematical function. We store only the **Hash** of the password. If the database is stolen, the attacker can't read the real passwords. Use **bcrypt** or **Argon2**.
13. **Q: What is a 'Man-in-the-Middle' (MITM) attack?**
    - **Answer**: When an attacker intercepts the communication between two systems. Prevent this by using **SSL/TLS** (HTTPS) for all API calls and verifying SSL certificates in `requests`.
14. **Q: What is 'Least Privilege' in a Python environment?**
    - **Answer**: Running your Python application with the **minimum** permissions it needs (e.g., a "Read-Only" database user or a Limited ServiceAccount in Kubernetes).
15. **Q: How do you perform 'Log Sanitization'?**
    - **Answer**: By adding filters to your logger that automatically remove or "Mask" sensitive data (like `sk-` API keys, credit card numbers, or passwords) before they are written to a file.
16. **Q: What is 'Cryptographic Salt' and why is it used?**
    - **Answer**: A random string added to a password before hashing. It ensures that two users with the same password have different hashes, making 'Rainbow Table' attacks impossible.
17. **Q: What is the difference between 'Symmetric' and 'Asymmetric' encryption?**
   - **Answer**: **Symmetric**: The same key is used to lock and unlock (fast). **Asymmetric**: different keys (Public/Private) are used to lock and unlock (secure for transferring data over the internet).
18. **Q: What is 'CVE' (Common Vulnerabilities and Exposures)?**
    - **Answer**: A public list of known security vulnerabilities. Senior engineers use tools like `pip-audit` to check their projects against this list daily.
19. **Q: What is 'XSS' (Cross-Site Scripting)?**
    - **Answer**: An attack where a malicious script is injected into a website. While Python is backend, you must **Escape** all user input before outputting it into HTML to prevent this.
20. **Q: How do you handle 'File Upload' security in Python?**
    - **Answer**: Never trust the filename. Use a standard library to "Sanitize" the filename, limit the file size, and check the file content (MIME type) before saving it to the disk.

---

[← Previous: Performance](24-performance-profiling.md) | [Next: Advanced OOP →](26-metaprogramming-descriptors.md)
