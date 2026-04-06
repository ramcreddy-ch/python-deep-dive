# 09. Python for DevOps & Automation — Production Deep Dive

> If you are writing bash scripts longer than 100 lines, you are accumulating technical debt. Bash lacks structured testability, type safety, and error handling. Moving automation to Python is standard in modern platform engineering, but it requires wrapping OS-level operations cleanly.

---

## 🔍 Core Automation Tooling

### The Subprocess Module (Correctly)
Executing shell commands in Python is notoriously done poorly. `os.system()` is deprecated. `subprocess` is powerful but can hang infinitely if not guarded.

```python
import subprocess
import shlex

def safe_shell_exec(command: str, timeout_sec: int = 30) -> str:
    """Production-grade shell executor"""
    # shlex safely splits the command to avoid injection attacks
    cmd_list = shlex.split(command)
    
    try:
        # check=True raises an exception if exit code != 0
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            check=True,  
            timeout=timeout_sec
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        # Logs the specific bash error stream
        print(f"FAILED (Exit {e.returncode}): {e.stderr.strip()}")
        raise
    except subprocess.TimeoutExpired:
        print(f"TIMEOUT: Command exceeded {timeout_sec}s")
        raise
```

### The `os` vs `pathlib` Debate
Stop using `os.path.join()`. `pathlib` provides an object-oriented interface to the filesystem, eliminating OS-specific slash (`/` vs `\`) bugs immediately.

```python
from pathlib import Path

# Legacy: os.path.join(os.path.dirname(__file__), "config", "app.yaml")
# Modern DevOps:
base_dir = Path(__file__).parent
config_file = base_dir / "config" / "app.yaml"

if config_file.exists() and config_file.is_file():
    # Read text instantly without 'with open()' boilerplate
    content = config_file.read_text()
```

---

## 🏭 Infrastructure as Code (IaC) via Python

You don't need HCL or YAML when you have Python.

### Pulumi / AWS CDK (Cloud Development Kit)
Modern DevOps uses imperative languages to generate declarative infrastructure. This allows `for` loops, if statements, and unit testing of your infrastructure.

```python
import pulumi
from pulumi_aws import s3

def create_environment_buckets(env_name: str, team_count: int):
    buckets = []
    # Loops and logic inside infrastructure!
    for i in range(team_count):
        bucket = s3.Bucket(
            f"ml-data-{env_name}-team-{i}",
            acl="private",
            tags={
                "Environment": env_name,
                "ManagedBy": "Pulumi Python"
            }
        )
        buckets.append(bucket)
    return buckets

dev_buckets = create_environment_buckets("dev", 3)
```

---

## 🔧 Building CLI Tools (Click & Typer)

Sysadmins hate dealing with `python script.py --help` built on `argparse` because the help menus look terrible and the code is verbose. We use `Typer` (based on Click and Pydantic).

```python
import typer
from pathlib import Path

app = typer.Typer(help="SRE Platform Automation CLI")

@app.command()
def deploy(
    cluster: str = typer.Option(..., help="Target EKS cluster"),
    force: bool = typer.Option(False, "--force", "-f", help="Bypass health checks")
):
    """Deploys workloads to specified cluster."""
    typer.echo(f"Deploying to {cluster}...")
    if force:
        typer.secho("WARNING: Force mode enabled", fg=typer.colors.RED)

@app.command()
def purge_logs(
    log_dir: Path = typer.Argument(..., exists=True, file_okay=False, dir_okay=True),
    days_old: int = 7
):
    """Deletes logs older than X days."""
    typer.echo(f"Purging logs in {log_dir} older than {days_old} days.")

if __name__ == "__main__":
    app()
```

---

## 🎯 Senior Engineer Interview Questions

**Q1: How do you prevent shell-injection attacks when wrapping a CLI tool with `subprocess`?**
> **Answer:** You must never pass `shell=True` combined with an unsanitized f-string or `.format()` string. If you do `subprocess.run(f"cat {user_input}", shell=True)` and a user inputs `file.txt; rm -rf /`, the server wipes itself. You avoid this by passing the command as a list of arguments `["cat", user_input]`, keeping `shell=False` (the default). If you must parse a raw string to a list dynamically, use `shlex.split()`.

**Q2: Write a Python script to find all files larger than 1GB in a specific directory hierarchy.**
> **Answer:**
> ```python
> from pathlib import Path
> 
> def find_huge_files(directory_path, min_gb=1):
>     min_bytes = min_gb * 1024**3
>     target_dir = Path(directory_path)
>     
>     # rglob walks the directory recursively
>     for file_path in target_dir.rglob('*'):
>         if file_path.is_file() and file_path.stat().st_size >= min_bytes:
>             print(f"{file_path} - {file_path.stat().st_size / 1024**3:.2f} GB")
> ```

**Q3: How does the Python AWS CDK differ from Terraform?**
> **Answer:** Terraform uses HCL (HashiCorp Configuration Language), a declarative specification. AWS CDK allows you to use an imperative language (Python, TypeScript) to dynamically define infrastructure. Under the hood, CDK synthesized your Python code into a massive declarative AWS CloudFormation JSON template, which is then applied by AWS. Thus, CDK gives you the power of loops, classes, and standard unit-testing (via `pytest`), while still executing safely via a declarative engine.

**Q4: We have thousands of servers. We want to execute a Python health-check script on all of them simultaneously without installing an agent everywhere. How do we do this?**
> **Answer:** I would use Ansible. Ansible is written in Python and is agentless; it operates entirely over SSH. We can write an Ansible Playbook that copies our Python script to the `/tmp` directory of the target fleet over SSH, executes `python3 /tmp/script.py`, captures the standard output, and returns it centrally to our orchestrator.

---

[← Previous: Concurrency](08-concurrency.md) | [Back to Index](../README.md) | [Next: Python for Cloud →](10-python-cloud.md)
