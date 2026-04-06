# 25. Advanced Security — Injection, RCE & Insecure Deserialization

> "A single security hole can cost a company its entire reputation and millions of dollars. An expert doesn't 'Add Security' at the end; they design it into the core of the application by treating every input as a potential attack."

---

## ❓ The 'Why' (High-Level)
Python is a powerful language, and that power can be used against you. If your web server accepts a filename from a user and opens it without checking, an attacker could read your private SSH keys. If your script uses `eval()` on a user's input, they can run **any code** they want on your server. A principal engineer knows that **Trust is the enemy of Security**.

---

## 🌱 Module 1: The Basics (Junior) — The Human Factor
The most basic security is not "Technical"—it's about hygiene.

### 1. Hardcoded Secrets (The Cardinal Sin)
**NEVER** put passwords, API keys, or database URLs in your source code.
```python
# Junior: bad
SECRET_KEY = "p@ssword123"

# Professional: good (using ENV variables)
import os
SECRET_KEY = os.getenv("APP_SECRET_KEY")
```

### 2. Input Validation
Check that data is what it says it is before moving forward.
- **Example**: If you expect a "User ID", check that it's actually a number before searching the database.

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — The Injection
Injection is the most common web attack. It happens when you mix "Data" with "Code."

### 1. SQL Injection
The most dangerous error is building a database query using an f-string.
- **BAD**: `f"SELECT * FROM users WHERE id={user_id}"`
- **EXPERT**: Use **Parameterized Queries**. The database driver keeps the query and the data separate, making it 100% immune to injection.
```python
# The Expert way (SQLAlchemy)
user = session.query(User).filter(User.id == user_id).first()
```

### 2. Cross-Site Scripting (XSS)
Always "Escape" user-generated content before showing it on a website, so an attacker can't inject a `<script>` that steals cookies.

---

## 🌳 Module 3: Advanced Mechanics (Senior) — RCE & Serialization
Senior engineers look for the "Silent Killers" that give an attacker full control.

### 1. RCE (Remote Code Execution)
RCE is the "Holy Grail" for hackers. It happens when an attacker can trick your Python server into running **their code**.
- **The Evils**: `eval()`, `exec()`, and `os.system()`. **NEVER** use these on data from a user.

### 2. Insecure Deserialization (`pickle`)
Python's `pickle` library is not safe. An attacker can craft a malicious "pickle file" that, when loaded, runs a shell command to delete your whole server.
- **Expert Fix**: Use **JSON** for data sharing. It's just text and cannot "run code."

---

## 🔥 Module 4: Principal Architect (Principal) — Platform Security
At the highest level, you protect the entire "Infrastructure" from the code.

### 1. Path Traversal
If your code does `open("/home/app/files/" + filename)`, an attacker can send a filename like `../../etc/passwd` to read your system's passwords.
- **Principal Choice**: Always use `os.path.basename()` to strip out the ".." parts.

### 2. Secure Secret Handling
A principal engineer uses a **Secrets Vault** (like AWS Secrets Manager or HashiCorp Vault) to rotate passwords automatically every 30 days without ever touching the source code.

---

## 🏗️ Case Study: The 20-Minute Zero-Day Fix
A major bank's security team noticed a "Shell Command" being run by their Python-based web server.
- **The Junior Approach**: Try searching the logs to see who did it. (Too slow, attacker was already inside).
- **The Principal Approach**: Used **Bandit** to scan the codebase and instantly found a developer had used `pickle.load()` for a "preferences file" uploaded by the user. They immediately deployed a patch that replaced `pickle` with `JSON`.
- **Result**: Stopped the attack before any customer data was stolen.

---

## ⚡ Anti-Patterns & Expert Traps

### 1. The `shell=True` Trap
When using `subprocess.run()`, setting `shell=True` allows an attacker to add a semicolon `;` and their own command to yours. **Expert fix**: Pass a **List** of arguments instead.

### 2. Running as `root`
Always run your Python application as a "Limited User" inside your container or server. If a hacker breaks into your app, they will only have limited permissions instead of "owning" the whole machine.

---

## 🎯 Top 20 Principal Interview Questions (Advanced Security)

1. **Q: What is 'SQL Injection' and how do you prevent it?**
   - **Answer**: it's an attack where a user inputs malicious SQL code into a form to bypass security or steal data. Prevent it by using **Parameterized Queries** or an **ORM** (like SQLAlchemy), which separates the code from the data.
2. **Q: Why is the `eval()` function considered extremely dangerous?**
   - **Answer**: it executes a string as literal Python code. If an attacker can control that string, they can run **any command** on your server, including deleting files or stealing data.
3. **Q: Explain the risk of using the `pickle` module.**
   - **Answer**: `pickle` files can execute code upon being loaded (`__reduce__` method). If you load a pickle file from an untrusted user, it can result in **Remote Code Execution (RCE)**.
4. **Q: What is 'Cross-Site Scripting' (XSS)?**
   - **Answer**: An attack where a malicious script (JavaScript) is injected into a trusted website. This is typically done by saving the script as user content (like a comment) which is then executed in the browsers of other visitors.
5. **Q: What is 'Path Traversal' and how do you mitigate it?**
   - **Answer**: An attack where a user tries to access files outside the intended directory (e.g., using `../../`). Mitigate it by using `os.path.basename()` or `pathlib.Path.resolve()` to validate the final path.
6. **Q: What does the `shell=True` flag in `subprocess.run()` do and why is it risky?**
   - **Answer**: It passes the command string to the system shell (e.g., `/bin/sh`). This is risky because it allows for **Shell Injection** if the string contains unvalidated user input.
7. **Q: How should you store 'Secrets' (Passwords/API Keys) for a production application?**
   - **Answer**: NEVER in the source code. Use **Environment Variables**, **Secret Managers** (AWS KMS/HashiCorp Vault), or **GitHub Secrets** for CI/CD pipelines.
8. **Q: Explain 'Insecure Deserialization'.**
   - **Answer**: The process of taking untrusted data (like a stream of bytes) and turning it back into an object. If the deserializer is powerful (like `pickle` or `yaml.load`), it can be tricked into running code.
9. **Q: What is 'CSRF' (Cross-Site Request Forgery)?**
   - **Answer**: An attack that tricks a logged-in user into performing an action they didn't intend (e.g., clicking a link that secretly sends a "Change Password" request to a site where they are logged in).
10. **Q: What is the purpose of 'Bandit' in a Python project?**
    - **Answer**: It is a security-focused **Linter** that scans Python source code for common security "Sins" like `shell=True`, hardcoded passwords, and use of insecure libraries.
11. **Q: How can you protect against 'Brute-Force' attacks?**
    - **Answer**: By implementing **Rate Limiting** (preventing too many requests from the same IP) and **Account Lockout policies**.
12. **Q: What is 'JWT' (JSON Web Token) and how should it be secured?**
    - **Answer**: A token used for authentication. It must be **Digitally Signed** using a strong secret and should ideally be stored in an `HttpOnly` cookie to prevent theft via XSS.
13. **Q: Why should an application ever be run as the `root` user?**
    - **Answer**: **NEVER**. If an attacker finds a vulnerability in a `root` application, they have full control over the entire operating system.
14. **Q: What is 'PII' and why is logging it dangerous?**
    - **Answer**: **Personally Identifiable Information** (e.g., email, SSN). Logging it is dangerous because logs are often stored in less secure developer environments, increasing the risk of a data breach.
15. **Q: Explain 'Security Headers' (like HSTS or CSP).**
    - **Answer**: Instructions sent by the server to the browser to enable security features (e.g., "Always use HTTPS" or "Only run scripts from this domain").
16. **Q: What is the risk of using `yaml.load()` without the `SafeLoader`?**
    - **Answer**: Similar to `pickle`, the standard YAML loader in old versions can be tricked into instantiating arbitrary Python objects, leading to Code Execution.
17. **Q: What is a 'Man-in-the-Middle' (MITM) attack and how do you prevent it?**
    - **Answer**: When an attacker intercepts the traffic between a client and a server. It is prevented by using **End-to-End Encryption** (HTTPS/TLS).
18. **Q: What is 'Data Masking'?**
    - **Answer**: The process of hiding or anonymizing sensitive data (e.g., `XXXX-XXXX-XXXX-1234`) when it is being viewed by people who don't need the full information.
19. **Q: How does 'Hashing' differ from 'Encryption'?**
    - **Answer**: **Hashing** is a one-way transformation (you can't "unhash" a password). **Encryption** is two-way (you can unlock it with a key). Passwords should ALWAYS be hashed.
20. **Q: What is 'Secrets Rotation' and why is it important at the principal level?**
    - **Answer**: The process of automatically changing passwords and keys on a schedule (e.g., every 90 days). This ensures that if a key is stolen, its usefulness is limited in time.

---

[Previous: Performance](24-performance-profiling.md) | [Next: Metaprogramming →](26-metaprogramming.md)
