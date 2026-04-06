# 16. Python for DevOps — Automation, CLIs & OS Scripts

> "A DevOps engineer is a developer who treats Infrastructure as Code. Expert Python DevOps engineers build CLIs, automate complex deployments, and manage system-level resources across thousands of servers with tools like `Click`, `Subprocess`, and `OS` modules."

---

## 🌱 The Basics: Shell & OS Interaction
The foundation of DevOps is calling existing shell commands and manipulating the file system.

```python
import os
import subprocess

# 1. Get current user and directory
user = os.getenv("USER")
cwd = os.getcwd()

# 2. Run a shell command safely
result = subprocess.run(["ls", "-lah"], capture_output=True, text=True)
# print(result.stdout)
```

---

## 🌿 Intermediate: Building Professional CLIs (Typer/Click)
Senior engineers don't just use `sys.argv`. They build real CLI tools with help menus, types, and flags.

**Real Use (Platform Tooling)**:
A command-line tool to manage a fleet of cloud servers.

```python
import typer

app = typer.Typer()

@app.command()
def deploy(env: str = "staging", force: bool = False):
    """
    Expert Pattern: CLI Interface. 
    Demonstrates: Clean, typed entry point for automation.
    """
    typer.echo(f"Starting deployment to {env}...")
    if force:
        typer.echo("Force flag detected. Bypassing safety checks.")

# if __name__ == "__main__": app()
```

---

## 🌳 Advanced: SSH & Remote Execution (Paramiko)
For infrastructure that doesn't have an API, you must use **SSH**.

**Real Use (System Administration)**:
A Python script that logs into 50 Linux servers to update a config file and restart a service.

```python
import paramiko

def remote_exec(host, command):
    """
    Expert Pattern: Remote Automation. 
    Demonstrates: Communicating over SSH securely.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect(host, username="admin", key_filename="~/.ssh/id_rsa")
    # stdin, stdout, stderr = ssh.exec_command(command)
    # print(stdout.read())
```

---

## 🔥 Expert: Configuration Management & YAML
Principal engineers avoid "Hardcoding" anything. They use **YAML** or **HCL** (HashiCorp Configuration Language) to drive their Python logic.

- **PyYAML**: The standard for parsing CI/CD and Kubernetes configuration files.

```python
import yaml

# Expert Pattern: Config Isolation. 
# 1. Load config from 'infra.yaml'.
# 2. Python creates the resources based on the file content.
```

---

## 🎯 Top 20 Principal Interview Questions (DevOps Engineering)

1. **Q: Why is `subprocess.run()` preferred over `os.system()`?**
   - **Answer**: `subprocess.run()` is more **Secure** (it avoids shell injection) and more **Powerful** (it captures `stdout` and `stderr` and allows for timeouts). `os.system()` is legacy and should be avoided in production.
2. **Q: What is the difference between `os.path` and the `pathlib` module?**
   - **Answer**: `os.path` uses strings and is manual for different operating systems. `pathlib` is **Object-Oriented** and cross-platform; it handles slashes (`/` vs `\`) automatically.
3. **Q: How do you handle 'Secret' credentials in a Python script safely?**
   - **Answer**: **Never** hardcode them. Use **Environment Variables** (`os.getenv`), a **Secret Manager** (like AWS Secrets Manager), or a **Vault** injection during the CI/CD pipeline.
4. **Q: Explain the 'Click' (or Typer) library.**
   - **Answer**: It is a framework for creating professional Command Line Interfaces (CLIs) with automatic help generation, argument validation, and sub-command support.
5. **Q: What is 'Infra as Code' (IaC) in the context of Python?**
   - **Answer**: Using Python to define and manage infrastructure components (like EC2 instances or S3 buckets) via APIs instead of manual console actions.
6. **Q: What is the purpose of the `shutil` module?**
   - **Answer**: High-level file operations like **Copying/Moving** entire directories and file trees that `os` doesn't handle easily.
7. **Q: How do you check if a specific process is running using Python?**
   - **Answer**: Use the **`psutil`** library to iterate through all active processes and filter by name or PID.
8. **Q: What is 'Sudo' and how do you handle it in a Python script?**
   - **Answer**: It allows running code with root privileges. In Python, you should ideally **avoid** running the whole script as sudo. Instead, use `subprocess` to call only specific commands that need elevated permissions.
9. **Q: Explain 'YAML' vs 'JSON' for configuration.**
   - **Answer**: JSON is for **Data Interchange** (API). YAML is for **Human Configuration** (DevOps tools like K8s, Ansible). YAML supports comments and is much easier for humans to read and edit.
10. **Q: How do you perform 'Bulk' operations on a file system using Python?**
    - **Answer**: Using `os.walk()` to recursively go through directories and files, or `glob.glob()` to find all files matching a specific pattern (e.g., `*.log`).
11. **Q: What is 'Idempotency' in a DevOps script?**
    - **Answer**: The quality of a script such that running it multiple times produces the same result as running it once. Example: A script that creates a folder only if it doesn't already exist.
12. **Q: How do you handle 'Cron Jobs' for Python scripts?**
    - **Answer**: By adding the script to the system crontab. Important: You must use the **Absolute Path** to both the internal `python` interpreter and the script file itself.
13. **Q: What is the purpose of `sys.argv`?**
    - **Answer**: A list containing the command-line arguments passed to a Python script. `sys.argv[0]` is always the script name itself.
14. **Q: What is 'Remote Execution'?**
    - **Answer**: The ability to run commands on a different server over a network (usually via **SSH** using the `Paramiko` library).
15. **Q: How do you avoid 'Deadlocks' in subprocess communication?**
    - **Answer**: Use `subprocess.communicate()` instead of reading from `stdout` and writing to `stdin` manually. It handles the buffering internally to prevent the process from hanging.
16. **Q: What is 'Ansible' and can you build custom modules for it in Python?**
    - **Answer**: Ansible is an automation engine. Yes, its modules are essentially Python scripts that accept JSON input and return JSON output.
17. **Q: What is the `tempfile` module?**
    - **Answer**: A safe way to create temporary files and directories that are automatically cleaned up when no longer needed.
18. **Q: How can you measure 'Execution Time' for a long-running automation task?**
    - **Answer**: Use the **`time.perf_counter()`** for high-precision measurement of wall-clock time.
19. **Q: What is the difference between `ls` and a Python `os.listdir()`?**
    - **Answer**: `ls` is an external shell command. `os.listdir()` is a built-in Python function that returns a list of files. Using the Python function is faster and more portable.
20. **Q: What is 'Linting' in a DevOps pipeline?**
    - **Answer**: Automatically checking your code for style and potential errors (using `flake8` or `pylint`) before it is ever allowed to be deployed.

---

[← Previous: Networking](15-networking-http.md) | [Next: Cloud →](17-python-cloud.md)
