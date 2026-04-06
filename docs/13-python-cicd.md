# 13. Python for CI/CD Pipelines — Production Deep Dive

> Modern Continuous Integration doesn't rely solely on bash scripts stapled inside YAML files. When logic gets complex (matrix testing, dynamic environment provisioning, dependency validation), we write the CI pipeline logic in Python. It's testable, structured, and cross-platform.

---

## 🔍 CI/CD Anti-Patterns

### The YAML Monolith
Writing 50 lines of bash inside a GitHub Action `run` block or a GitLab CI `script` block is unmaintainable. Syntax highlighting breaks, quote escaping is a nightmare, and you cannot test it locally without committing and pushing to the server.

```yaml
# THE ANTI-PATTERN (Dagger/Bash in YAML)
jobs:
  build:
    steps:
      - run: |
          if [ -d "src" ]; then
            for file in src/*.py; do
              # Complex logic string parsing...
              echo "Processing $file"
            done
          fi
```

### The Python Solution
Extract logic into standalone Python scripts. The YAML file should only be responsible for configuring the environment and calling the script.

```yaml
# THE PRODUCTION PATTERN
jobs:
  build:
    steps:
      - run: python .github/scripts/validate_build.py --env staging
```

---

## 🏭 Standardizing Automation Tools

### 1. Invoke (The Python Makefile)
Makefiles are great, but managing cross-platform compatibility (Windows vs Linux) and complex dependencies is hard. The `invoke` library replaces Makefiles with Python.

```python
# tasks.py (Placed in repo root)
from invoke import task
import os

@task
def install(c):
    """Install dependencies"""
    c.run("pip install -r requirements.txt")

@task(install) # 'lint' implicitly requires 'install' to run first!
def lint(c, fail_under=9.0):
    """Run pylint with a strict threshold"""
    print("Running strict linting...")
    result = c.run(f"pylint src/ --fail-under={fail_under}", warn=True)
    if result.exited != 0:
        print("Linting failed!")
        raise SystemExit(1)

@task
def deploy(c, env="dev"):
    """Deploy to Kubernetes"""
    if env not in ["dev", "staging", "prod"]:
        raise ValueError("Invalid environment")
    c.run(f"helm upgrade --install my-app ./chart -f values-{env}.yaml")
```
*Usage from terminal: `inv lint` or `inv deploy --env prod`*

### 2. Pre-Commit Hooks
Don't let bad code reach the CI server. Fail it on the developer's laptop during `git commit`.

```yaml
# .pre-commit-config.yaml
repos:
-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black
-   repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
    -   id: flake8
-   repo: local  # Custom Python script!
    hooks:
    -   id: check-aws-creds
        name: Catch hardcoded AWS Keys
        entry: python scripts/detect_secrets.py
        language: system
        files: \.py$
```

---

## 🤖 MLOps Application (Continuous Training Pipelines)

In standard DevOps, CI/CD builds a Docker image. In MLOps, CI/CD often triggers a model re-training job on Vertex AI or Amazon SageMaker via Python SDKs.

### Pytest for Machine Learning
We don't just unit-test code; we unit-test models.

```python
import pytest
import pandas as pd
from my_model_pipeline import load_model, predict

@pytest.fixture
def test_dataset():
    # Load a small, deterministic subset of data
    return pd.read_csv("tests/data/golden_set.csv")

def test_model_accuracy_regression(test_dataset):
    """Fails the CI pipeline if the new model performs worse than the baseline"""
    model = load_model("latest")
    
    X = test_dataset.drop('target', axis=1)
    y_true = test_dataset['target']
    
    y_pred = model.predict(X)
    accuracy = (y_pred == y_true).mean()
    
    # Assert new model meets minimum baseline (90%)
    assert accuracy >= 0.90, f"Model degradation! Accuracy dropped to {accuracy}"

def test_inference_latency(test_dataset):
    """Prevents deploying slow models (e.g. LLMs) to production"""
    import time
    model = load_model("latest")
    
    start = time.perf_counter()
    model.predict(test_dataset.iloc[[0]]) # Single prediction
    duration_ms = (time.perf_counter() - start) * 1000
    
    # API SLA is 100ms
    assert duration_ms < 100, f"Latency violation: {duration_ms}ms"
```

---

## 🎯 Senior Engineer Interview Questions

**Q1: How do you pass state between different Jobs in a GitLab CI or GitHub Action pipeline using Python?**
> **Answer:** Pipeline steps are naturally isolated (often running on completely different runner VMs). To pass state from a Python script in Job A to Job B, we serialize the data and write it to disk. We then instruct the CI platform to upload that file as an "artifact" attached to the build. Job B then downloads the artifact, and its Python script reads the file from disk to resume the context. A more advanced pattern is pushing the state to a remote Redis or AWS SSM Parameter Store.

**Q2: We need to pull private packages from an internal Nexus/Artifactory pip repository during the CI Docker build. How do you pass the credentials securely without baking them into the Docker image layers?**
> **Answer:** Never use `ENV` or `ARG` for secrets in Dockerfiles because they remain permanently readable in the image history. Instead, we use Docker BuildKit's `--secret` mounting. In the CI pipeline, we pass the token via CLI, and in the Dockerfile we use `RUN --mount=type=secret,id=pip_token pip install -i "https://$(cat /run/secrets/pip_token)@nexus.com/pypi" my_package`. This executes the install and immediately discards the secret from the resulting layer.

**Q3: Describe how you would implement a "Canary Analysis" script in Python for a Kubernetes deployment.**
> **Answer:** After the CI/CD pipeline shifts 10% of traffic to the new Canary pod, the Python script would run a continuous `while` loop for 5 minutes. Every 10 seconds, it queries the Prometheus API for both the `baseline` HTTP 500 error rate and the `canary` error rate. It runs a statistical comparison (e.g., Mann-Whitney U test) using `scipy`. If the canary deviation is statistically significant and negative, the script exits with code 1, which causes the CI/CD pipeline to trigger an automatic Helm rollback.

**Q4: Look at this `pytest` run: `pytest tests/ --numprocesses 4`. How does `pytest-xdist` parallelize tests, and what is the biggest risk?**
> **Answer:** `pytest-xdist` uses the `execnet` library to spawn multiple Python worker processes and distributes individual tests to them. Because it uses processes, the tests run in isolated memory spaces, bypassing the GIL. The massive risk is state mutation. If two parallel tests rely on the same shared external resource (like a specific row in a staging database or a temporary local file), they will cause race conditions and flaky test failures. We fix this by writing strict teardown fixtures or mocking external state entirely.

---

[← Previous: Python for K8s](12-python-kubernetes.md) | [Back to Index](../README.md) | [Next: Networking & HTTP →](14-networking-http.md)
