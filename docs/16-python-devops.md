# 16. Python for DevOps — Automation, Subprocess & Typer CLIs

> "DevOps is the art of automating your job away. An expert doesn't just write scripts; they build robust, self-healing CLI tools that handle errors, timeouts, and security risks like Shell Injection. If it's done more than twice, it should be a Python script."

---

## ❓ The 'Why' (High-Level)
In modern Platform Engineering, there is no "Manual Work." If you need to back up a database, rotate a log, or deploy a container, you write a script to do it. Why Python? because it's cross-platform, has a huge ecosystem (Boto3, Kubernetes-client), and is much easier to maintain than a 500-line Bash script. A principal engineer knows that **Automation is the only way to scale**.

---

## 🌱 Module 1: The Basics (Junior) — Talking to the OS
The most basic DevOps task is running a command and checking an environment variable.

### 1. Environment Variables
```python
import os
db_url = os.getenv("DATABASE_URL", "localhost")  # Always set a default!
```

### 2. Basic Shell Commands
```python
import subprocess
# The Junior way to run a command
subprocess.run(["ls", "-l"])
```

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — The CLI
Mid-level engineers don't hardcode values; they allow the user to pass them as **Arguments**.

### 1. Building a CLI with `argparse`
```python
import argparse
parser = argparse.ArgumentParser(description="Backup a directory")
parser.add_argument("source")
parser.add_argument("--dest", default="/tmp/backup")
args = parser.parse_args()
```

### 2. Capturing Output
Professional scripts don't just "print" to the screen—they capture the output for later processing.
```python
result = subprocess.run(["git", "status"], capture_output=True, text=True)
if result.returncode == 0:
    print(result.stdout)
```

---

## 🌳 Module 3: Advanced Mechanics (Senior) — Modern Automation
Senior engineers use cutting-edge libraries to build "Beautiful" CLIs.

### 1. Building CLIs with `Typer`
**Typer** uses Python type hints to generate help docs and auto-completion.
```python
import typer

def main(name: str, count: int = 1):
    for _ in range(count): print(f"Hello {name}")

if __name__ == "__main__":
    typer.run(main)
```

### 2. Advanced Subprocess: Timeouts & Pipes
Prevent your script from hanging forever if a command gets stuck.
```python
try:
    subprocess.run(["long_task"], timeout=30)
except subprocess.TimeoutExpired:
    print("Task took too long!")
```

---

## 🔥 Module 4: Principal Architect (Principal) — Safety & Signals
At the highest level, your scripts must be as stable as the systems they manage.

### 1. The Death of `shell=True` (Security)
**NEVER** use `shell=True` in production. It allows for **Shell Injection** attacks, where an attacker can run `rm -rf /` by passing a specially crafted filename.
- **Principal Choice**: Always pass a **List** of arguments: `["ls", "-l", folder]`.

### 2. Graceful Shutdowns (Signals)
If your automation script is long-running (like a watcher), it must handle `SIGTERM` signals from the OS to shut down cleanly without losing data.

---

## 🏗️ Case Study: The Multi-Cluster Management Tool
A global bank needed a tool for 500 SREs to manage 100 Kubernetes clusters across AWS and GCP.
- **The Junior Approach**: A folder full of 20 different Bash scripts (hard to version and update).
- **The Principal Approach**: Built a single **Unified Python CLI** using `Typer`. It included a "Dry Run" mode to show what would happen before actually changing anything.
- **Result**: Reduced accidental infrastructure deletions by 90% and saved the SRE team 10 hours a week in troubleshooting.

---

## ⚡ Anti-Patterns & Expert Traps

### 1. Hardcoding Paths
Don't use `C:\Users\Ram\data`. Use `Path.home()` or environmental variables like `APPDATA`.

### 2. Ignoring Non-Zero Exit Codes
By default, `subprocess.run` won't tell you if a command failed. **Expert fix**: Use `check=True` to immediately raise an exception if the command crashes.

---

## 🎯 Top 20 Principal Interview Questions (Python for DevOps)

1. **Q: Why use Python instead of Bash for complex automation?**
   - **Answer**: Python provides better error handling, data structures (lists/dicts), cross-platform support, and unit testing capabilities, making large scripts easier to maintain.
2. **Q: What is the main risk of using `os.system()`?**
   - **Answer**: It is **obsolete** and insecure. It doesn't capture output, doesn't handle errors well, and is prone to **Shell Injection** because it passes raw strings to the terminal.
3. **Q: What is 'Shell Injection' and how do you prevent it in Python?**
   - **Answer**: A security vulnerability where an attacker adds malicious commands to a string passed to the shell. Prevent it by passing arguments as a **List** to `subprocess.run` and never using `shell=True`.
4. **Q: Explain the difference between `subprocess.run()`, `call()`, and `check_output()`.**
   - **Answer**: `run()` is the modern (3.5+) standard that covers almost all use cases. `call()` is legacy (only returns the exit code). `check_output()` is legacy (only returns the stdout).
5. **Q: What does the `check=True` parameter do in `subprocess.run()`?**
   - **Answer**: it tells Python to raise a `CalledProcessError` if the subprocess exits with a non-zero status (i.e., it failed), ensuring the script doesn't just continue blindly.
6. **Q: How can you capture both `stdout` and `stderr` in a single variable?**
   - **Answer**: By setting `stdout=subprocess.PIPE` and `stderr=subprocess.STDOUT` (which redirects error to output).
7. **Q: What is the `shutil` module used for?**
   - **Answer**: For high-level **File Operations** like copying whole directories (`copytree`), moving files (`move`), and checking disk space (`disk_usage`).
8. **Q: Explain the purpose of `os.environ`.**
   - **Answer**: It is a dictionary-like object representing the current system environment variables. It's used to read configurations (like DB passwords) without hardcoding them.
9. **Q: What is 'Typer' and why is it preferred over `argparse`?**
   - **Answer**: It's a library for building CLIs based on **Python Type Hints**. It results in much less code, automatic help page generation, and better auto-completion.
10. **Q: How do you handle 'Timeouts' in a subprocess?**
    - **Answer**: By passing the `timeout` parameter (in seconds) to `subprocess.run()`. It will raise a `TimeoutExpired` exception if the command takes too long.
11. **Q: What is the `sys.argv` list?**
    - **Answer**: A list containing the command-line arguments passed to the script, where `sys.argv[0]` is always the script name itself.
12. **Q: How do you run a command in the 'Background' without waiting for it to finish?**
    - **Answer**: Use `subprocess.Popen()`. This creates the process and continues your script immediately; you can later check its status or call `.wait()`.
13. **Q: Explain 'Piping' between two commands in Python.**
    - **Answer**: Creating two `Popen` objects and setting the `stdout` of the first to be the `stdin` of the second (equivalent to `ls | grep` in Bash).
14. **Q: What is `sys.exit()` and how does it differ from `exit()`?**
    - **Answer**: `sys.exit()` is the professional way to stop a script and return a status code. `exit()` is meant for the interactive REPL and should not be used in production scripts.
15. **Q: How can you make a Python script executable as a global command?**
    - **Answer**: By adding a **Shebang** line (`#!/usr/bin/env python3`), setting the file permission to executable, and optionally adding it to the system's `PATH`.
16. **Q: What is the purpose of the `signal` module?**
    - **Answer**: To handle inter-process signals like `SIGINT` (Ctrl+C) so the script can close database connections or save files before exiting.
17. **Q: How do you check if a specific command exists on the user's machine?**
    - **Answer**: By using `shutil.which("command_name")`, which returns the path to the executable if found, or `None` if not.
18. **Q: What is 'Dry Run' mode and why is it important in DevOps?**
    - **Answer**: A flag (e.g., `--dry-run`) that shows what a script **would** do without actually making any changes, preventing accidental infrastructure destruction.
19. **Q: How do you change the Working Directory of a subprocess?**
    - **Answer**: By passing the `cwd` (Current Working Directory) parameter to `subprocess.run()`.
20. **Q: What is the difference between `os.path` and `pathlib` for DevOps?**
    - **Answer**: `os.path` works with strings; `pathlib` works with **Objects**. `pathlib` is safer, cleaner, and handles cross-platform path issues automatically.

---

[Previous: Networking](15-networking-http.md) | [Next: Python for Cloud →](17-python-cloud-boto3.md)
