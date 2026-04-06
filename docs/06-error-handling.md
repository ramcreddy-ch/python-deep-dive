# 06. Error Handling & Debugging — Production Deep Dive

> "Never catch an exception you don't know how to handle." In SRE and DevOps, suppressing tracebacks creates ghost bugs. A crashed system is vastly superior to a system running in a corrupted zombie state. Production error handling is about graceful degradation, precise telemetry, and fail-fast architectures.

---

## 🔍 Core Exception Models

### The Hierarchy
All built-in, non-system-exiting exceptions inherit from `Exception`. `BaseException` is the root, which includes things like `KeyboardInterrupt` (Ctrl+C) and `SystemExit`.

```python
# The Ultimate Anti-Pattern (Catching BaseException/Broad Exception)
try:
    connect_to_db()
except Exception as e:
    pass # Silent failure! Logging an error but continuing is also often an anti-pattern.
```

### Contextualized Excepts
Catch only what you anticipate. Bubble up the rest.

```python
import requests

def fetch_k8s_metrics(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status() # Raises HTTPError for 4XX/5XX
    except requests.exceptions.Timeout:
        # We know how to handle timeout -> Return cached data or emit warning metric
        return load_cached_metrics()
    except requests.exceptions.HTTPError as err:
        # We know how to handle Auth errors -> Trigger alert
        trigger_pagerduty(f"Metrics API Failed: {err}")
        raise # Still raise because the flow cannot proceed
```

---

## 🏭 Production Reliability Patterns

### Custom Exception Architectures
Instead of raising generic `ValueErrors` inside your platform SDKs, build a semantic exception domain. This allows the calling API layer to map specific errors to HTTP Status Codes easily.

```python
# core/exceptions.py
class PlatformError(Exception):
    """Base exception for all internal platform errors."""
    pass

class ClusterNotFoundError(PlatformError):
    def __init__(self, cluster_id: str):
        self.cluster_id = cluster_id
        super().__init__(f"Kubernetes cluster '{cluster_id}' not found.")

class InsufficientGPUQuotaError(PlatformError):
    pass

# When the API layer catches these:
try:
    provision_training_job(data)
except ClusterNotFoundError:
    return {"error": "Invalid Cluster"}, 404
except InsufficientGPUQuotaError:
    return {"error": "Quota Exceeded"}, 429
```

### Traceback Management and Telemetry
`print(e)` loses the stack trace. `logging.error(e)` logs the string representation of the error, but loses the stack trace. 

**Always use `logging.exception()`** inside an except block.

```python
import logging

try:
    1 / 0
except ZeroDivisionError:
    # Captures the full traceback automatically and sends it to your STDOUT stream 
    # to be picked up by Datadog/ELK
    logging.exception("Failed to calculate deployment metrics")
```

---

## 🔧 DevOps & SRE Perspectives

### Retry Decorators (Tenacity)
DevOps tools battle network partitions constantly. AWS API throttles, Kubernetes API latency—we expect them to fail. Implement systematic retries. 

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from botocore.exceptions import ClientError

# Exponential backoff (wait 2^x * 1 second), stop after 5 tries
# ONLY retry if it's an AWS ClientError (like rate limiting)
@retry(
    stop=stop_after_attempt(5), 
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(ClientError)
)
def drain_k8s_node(node_name):
    print(f"Attempting to drain {node_name}...")
    # Cloud API call here...
    raise ClientError({"Error": {"Code": "Throttling"}}, "Terminate")

# Calling it will auto-retry gracefully
```

### Contextlib: suppress
If you explicitly intend to ignore an exception natively, standard library provides a cleaner way than `try/pass`.

```python
from contextlib import suppress
import os

# Removes file if it exists, doesn't crash if it doesn't.
with suppress(FileNotFoundError):
    os.remove('/tmp/stale_lock.pid')
```

---

## 🤖 MLOps / AI Perspective

### Handling OOM (Out Of Memory) Gracefully
PyTorch/CUDA OOM errors are legendary. We catch them to release memory and attempt recovery (like reducing batch size on the fly).

```python
import torch

batch_size = 128
while batch_size > 0:
    try:
        # Simulate moving batch to GPU
        inputs = torch.randn(batch_size, 3, 224, 224).cuda()
        break # Success! Break out of retry loop
    except torch.cuda.OutOfMemoryError:
        print(f"CUDA OOM at batch size {batch_size}. Halving and retrying...")
        
        # Crucial: Must empty cache before retrying otherwise memory remains fragmented
        torch.cuda.empty_cache() 
        batch_size //= 2

if batch_size == 0:
    raise RuntimeError("Model too large to fit on GPU even at batch_size=1")
```

---

## 🎯 Senior Engineer Interview Questions

**Q1: Explain the difference between `BaseException` and `Exception`. Why do we inherit custom errors from `Exception`?**
> **Answer:** `BaseException` is the top-level root for all exceptions, including system-interrupting events like `SystemExit` (triggered by `sys.exit()`) and `KeyboardInterrupt` (Ctrl+C). `Exception` inherits from `BaseException` and represents non-fatal, programmatic errors. We inherit custom errors from `Exception` and we only use `except Exception:` in code so that we aren't accidentally trapping and blocking server shutdown commands or keyboard interrupts, which would make our daemons unkillable.

**Q2: What is the purpose of `raise ... from e` in Python 3?**
> **Answer:** It defines Exception Chaining. When you catch an exception (like a low-level psycopg2 DatabaseError) and re-raise it as a higher-level domain error (like a DataRetrievalError), writing `raise DataRetrievalError() from e` links the two tracebacks. In the logs, you will see exactly what domain error occurred and explicitly what low-level error triggered it, making root-cause analysis immensely faster.

**Q3: How would you debug a silent memory leak in a long-running Kubernetes Python container?**
> **Answer:** Assuming code tracing isn't enough, I'd attach profiling tools. First, I'd expose a `tracemalloc` endpoint in the Flask/FastAPI app to take snapshots of memory allocations over time and diff them to find what line of code is allocating undropped objects. Additionally, tools like `objgraph` or `py-spy` can be attached to the running PID inside the container to visualize the reference cycles that the garbage collector is failing to clean up. 

**Q4: Look at this code: `try: foo() finally: bar()`. If `foo()` raises a ValueError, what happens to `bar()`? What if `foo()` calls `os._exit(1)`?**
> **Answer:** The `finally` block *always* executes, regardless of whether `foo()` succeeds, raises an exception, or even returns early. Thus, `bar()` will execute, and then the original `ValueError` will continue propagating up the stack. However, if `foo()` hits `os._exit(1)`, this bypasses Python's normal termination process entirely, exiting at the C level immediately; `bar()` will **not** execute.

---

[← Previous: File I/O](05-file-io-serialization.md) | [Back to Index](../README.md) | [Next: Decorators & Generators →](07-decorators-generators.md)
