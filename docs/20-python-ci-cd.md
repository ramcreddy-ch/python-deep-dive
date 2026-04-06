# 20. Python for CI/CD — GitHub Actions, Jenkins & Automation

> "A manual deployment is a point of failure. Expert CI/CD Engineers use Python to build 'Self-Verifying' pipelines — automating the entire journey from Git Commit to Production Deployment with absolute zero human intervention."

---

## 🌱 The Basics: Automation Scripts in CI
The entry-level way to use Python in CI/CD is as a simple **Check** script.

```yaml
# GitHub Actions snippet
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Run Python Check
        run: |
          python -m pip install -r requirements.txt
          python tests/verify_integrity.py
```

---

## 🌿 Intermediate: GitHub Actions & Environment Variables
Senior engineers use Python to **dynamically** generate their CI/CD state based on the environment (Dev, Staging, Prod).

**Real Use (Platform/DevOps)**:
A Python script that reads the branch name and automatically sets the AWS S3 Bucket destination for the build.

```python
import os

def set_ci_env():
    """
    Expert Pattern: Dynamic Configuration. 
    Demonstrates: Mapping Git State to Cloud State.
    """
    branch = os.getenv("GITHUB_REF_NAME")
    if branch == "main":
        print("::set-output name=BUCKET::prod-static-site")
    else:
        print("::set-output name=BUCKET::dev-static-site")
```

---

## 🌳 Advanced: Automated Deployment (Hooks)
Instead of just "Running" a script, an expert uses **Hooks**.

- **Pre-Commit Hooks**: runs Python checks (like `black` for formatting or `flake8` for linting) **before** code is even allowed to be committed to the machine.
- **Webhooks**: A Python API (FastAPI) that "Listens" for a Git Push and automatically triggers a Jenkins job or a K8s deployment.

---

## 🔥 Expert: The 'Self-Healing' Pipeline
Principal engineers build pipelines that **test themselves**.

### 1. Progressive Rollouts (Canary)
A Python script that deploys a new version to only 5% of users. It then "Watches" Prometheus. If the error rate stays at zero for 10 minutes, it automatically scales to 100%.

### 2. Automated Rollback
If the Python script detects a CPU spike > 90% during the deployment, it instantly calls the Kubernetes API to **Rollback** the deployment to the previous stable version.

---

## 🎯 Top 20 Principal Interview Questions (CI/CD)

1. **Q: What is the benefit of using Python over Bash in a CI/CD pipeline?**
   - **Answer**: Python is more **Readable**, has better **Error Handling**, and provides sophisticated libraries for JSON/YAML parsing and Cloud API interaction (Boto3). Bash becomes messy once the logic exceeds 10-20 lines.
2. **Q: What is a 'Pre-Commit' hook?**
   - **Answer**: A local script that automatically runs checks (like linting or unit tests) before a developer is allowed to `git commit` their code. It prevents "Junk" code from ever reaching the server.
3. **Q: How do you handle 'Secrets' (API Keys) in a GitHub Action safely?**
   - **Answer**: Store them in **GitHub Secrets** and inject them as **Environment Variables** in the `.yaml` workflow file. Never print them to the logs.
4. **Q: What is a 'Linter' (like Flake8) and why is it mandatory in CI?**
   - **Answer**: A linter checks your code for **Style and Quality** (e.g., unused imports, long lines). It ensures that a team of 100 developers all write code that looks like it was written by one person.
5. **Q: Explain 'Continuous Integration' (CI) vs 'Continuous Deployment' (CD).**
   - **Answer**: **CI** is the practice of automatically building and testing code on every push. **CD** is the practice of automatically deploying that code to production once it passes all tests.
6. **Q: What is a 'Build Artifact'?**
   - **Answer**: The final, deployable file produced by a CI pipeline (e.g., a `.whl` Wheel file, a `.zip` Lambda package, or a Docker Image).
7. **Q: How do you perform 'Self-Healing' in a pipeline?**
   - **Answer**: By adding a monitoring step after deployment. If Python detects high error rates or latency via an API (Prometheus), it automatically triggers a **Rollback** command.
8. **Q: What is a 'Unit Test' vs 'Smoke Test' in a pipeline context?**
   - **Answer**: **Unit Test**: Checks a single function (run during the Build phase). **Smoke Test**: A fast, high-level check on the live server (run during the Deploy phase) to verify the app is "Up" and responding.
9. **Q: How do you handle 'Dependency Caching' in CI to speed up builds?**
   - **Answer**: By using the CI provider's caching action to store the `~/.cache/pip` or `poetry` directory, so dependencies aren't re-downloaded on every single run.
10. **Q: What is a 'Matrix Build'?**
    - **Answer**: Running the same CI pipeline across **Multiple Python Versions** (e.g., 3.9, 3.10, 3.11) simultaneously to ensure compatibility.
11. **Q: Explain the purpose of `pip-audit` in a security pipeline.**
    - **Answer**: It scans your `requirements.txt` for any libraries that have **Known Security Vulnerabilities** (CVEs) and fails the build if any are found.
12. **Q: What is a 'Webhook' and how can Python use it?**
    - **Answer**: An HTTP callback. A Python FastAPI server can "Listen" for a webhook from GitHub and automatically trigger a custom build or update a Jira ticket.
13. **Q: How do you automate 'Database Migrations' in CD?**
    - **Answer**: Running an Alembic (SQLAlchemy) migration script as a pre-deployment step. If the migration fails, the deployment is cancelled.
14. **Q: What is the difference between 'Gated' and 'Automatic' deployments?**
    - **Answer**: **Gated**: Deployment requires a human to click "Approve" (used for Production). **Automatic**: Deployment happens instantly once tests pass (used for Dev/Staging).
15. **Q: What is the purpose of `isort` and `black` in a pipeline?**
    - **Answer**: `isort` automatically sorts your imports alphabetically. `black` is an "Uncompromising" code formatter that automatically reformats your code to follow a strict style.
16. **Q: How do you handle 'Flaky Tests' in CI?**
    - **Answer**: By using the `pytest-rerunfailures` plugin to automatically retry a failed test once or twice, though the real goal should be to fix the underlying non-determinism.
17. **Q: What is 'Integration Testing' in a CI context?**
    - **Answer**: Spinning up a real (but temporary) database or service (using Docker) and running tests that check if your code can actually talk to it correctly.
18. **Q: How do you build a 'Canary' deployment with Python?**
    - **Answer**: A Python-controlled load balancer or K8s Service that directs only 5% of traffic to the new version while monitoring logs for errors.
19. **Q: What is the purpose of the `GITHUB_TOKEN`?**
    - **Answer**: A temporary, automatic authentication token provided by GitHub Actions that allows your Python script to update the repository (e.g., committing a new version number).
20. **Q: How do you handle 'Rollbacks' in a sophisticated CD pipeline?**
    - **Answer**: You must keep a **Registry** of previous stable build artifacts (Images/Wheels). If a failure is detected, Python "Re-deploys" the previous known-good version.

---

[← Previous: Kubernetes](19-python-kubernetes.md) | [Next: Data Engineering →](21-data-engineering.md)
