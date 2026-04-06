# 07. Decorators, Generators & Context Managers — Production Deep Dive

> These three features elevate Python code from procedural scripting mechanisms to professional, declarative platform engineering. Mastering them allows you to write middleware, control explosive memory footprints via lazy evaluation, and guarantee resource cleanup.

---

## 🔍 Decorators (Metaprogramming)

A decorator is a function that takes another function, extends its behavior without explicitly modifying it, and returns a new function. Extensively used in web frameworks (FastAPI `@app.get`) and access control.

### The Standard Pattern & functools.wraps
If you don't use `@wraps`, the decorated function loses its `__name__` and `__doc__` metadata, breaking debugging and auto-documenting APIs (like Swagger).

```python
import time
from functools import wraps

def time_execution(func):
    """SRE Decorator to track execution time of complex operations"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        # Execute the actual function
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        
        # We could push this to Prometheus/Datadog here
        print(f"Metric: [func:{func.__name__} | duration:{duration:.4f}s]")
        return result
    return wrapper

@time_execution
def spin_up_cluster():
    """Simulates cluster creation"""
    time.sleep(1.2)
    return "cluster-1a"

spin_up_cluster()
# Output: Metric: [func:spin_up_cluster | duration:1.2014s]
```

### Parameterized Decorators
Sometimes the decorator needs its own arguments (e.g., `@retry(attempts=3)`). This requires a 3-tier nested function.

```python
def authorize_rbac(required_role):
    def decorator(func):
        @wraps(func)
        def wrapper(user, *args, **kwargs):
            if user.get("role") != required_role:
                raise PermissionError("RBAC Denied")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator

@authorize_rbac(required_role="ml-admin")
def delete_model_registry(user):
    pass
```

---

## 🏭 Generators (Lazy Evaluation)

Generators `yield` values one at a time and suspend their state. They are mandatory when dealing with datasets that exceed system RAM.

### Creating Pipelines
We use generators to stream data directly from S3, parse it, and ingest it to a DB without ever holding more than 1 row in memory.

```python
def stream_s3_file(bucket_key):
    """Simulates pulling lines from S3 infinitely"""
    mock_lines = ["log1", "log2", "log3"]
    for line in mock_lines:
        yield line # Pauses here!

def filter_errors(log_stream):
    """Pulls from a stream, parses, and pushes to next stream"""
    for line in log_stream:
        if "ERROR" in line:
            yield line

# Memory footprint is essentially ~0MB regardless of file size
for errored_log in filter_errors(stream_s3_file("app.log")):
    send_to_elasticsearch(errored_log)
```

### Generator Expressions
Like list comprehensions, but wrapped in parenthesis `()`. They do not allocate memory for the list.

```python
import sys

# List comprehension: Computes immediately. RAM size: ~80,000 bytes
mem_heavy = [x**2 for x in range(10000)]

# Gen expression: Returns a tiny generator object. RAM size: ~104 bytes
mem_light = (x**2 for x in range(10000)) 
```

---

## 🔧 Context Managers (Resource Control)

The `with` statement ensures the `__enter__` and `__exit__` methods fire, regardless of crashes. In DevOps, we use this for database locks, network sessions, and local temporary files.

### Class-Based Context Managers

```python
class K8sClusterLock:
    def __init__(self, cluster_name):
        self.cluster_name = cluster_name
        
    def __enter__(self):
        print(f"Acquiring etcd lock for {self.cluster_name}")
        return self # This binds to the 'as' variable
        
    def __exit__(self, exc_type, exc_value, traceback):
        # Fires even if code inside 'with' crashes
        print(f"Releasing etcd lock for {self.cluster_name}")
        # If exc_type is not None, an error occurred. 
        # Returning True acts as a try/except catch. Returning False pushes it up.
        return False 

with K8sClusterLock("prod-us-east"):
    print("Performing sensitive upgrade...")
    # lock implicitly released here
```

### Contextlib's `@contextmanager`
Writing boilerplate classes is annoying. Standard library lets us convert a generator into a context manager.

```python
from contextlib import contextmanager
import os

@contextmanager
def temporary_env_variable(key, value):
    """Temporarily overrides an OS environment variable."""
    old_value = os.environ.get(key)
    os.environ[key] = value
    try:
        yield # The context block runs here
    finally:
        # Cleanup
        if old_value is None:
            del os.environ[key]
        else:
            os.environ[key] = old_value

with temporary_env_variable("AWS_REGION", "eu-west-1"):
    # Boto3 client built here will use eu-west-1
    pass 
# Boto3 goes back to original region outside block
```

---

## 🤖 MLOps Application: PyTorch Dataloaders
Under the hood, PyTorch `DataLoader` objects are heavily engineered generators. They chunk massive distributed disk pools, offload the text-to-tensor parsing to multi-core C++ workers, and `yield` batched tensors directly onto the GPU in time for the training loop forward pass.

```python
for batch in train_dataloader:
    # `batch` was `yield`ed by the loader processes.
    inputs, targets = batch['image'].to(device), batch['label'].to(device)
    optimizer.zero_grad()
    loss = model(inputs)
    # ...
```

---

## 🎯 Senior Engineer Interview Questions

**Q1: Write a decorator that caches (memoizes) the result of a function based on its arguments. (Bonus: how does the stdlib do this?)**
> **Answer:** 
> ```python
> def memoize(func):
>     cache = {}
>     def wrapper(*args):
>         if args not in cache:
>             cache[args] = func(*args)
>         return cache[args]
>     return wrapper
> ```
> Bonus: The standard library implements this robustly via `functools.lru_cache` (or `@cache` in modern Python). It caches the data but also implements a Least Recently Used eviction policy to prevent the cache from eating all host RAM.

**Q2: What happens if a `yield` statement is placed inside a `finally` block of a generator?**
> **Answer:** It's considered an advanced anti-pattern. If the generator is closed early (using `generator.close()`), a `GeneratorExit` exception is injected at the line where the generator is currently yielded. Python will jump to the `finally` block to execute cleanup. If the `finally` block contains another `yield`, Python raises a `RuntimeError: generator ignored GeneratorExit`, because a generator actively being destroyed is not legally permitted to yield a new value to the caller.

**Q3: How does a context manager handle exceptions raised within its `with` block?**
> **Answer:** If an exception occurs, the `__exit__` method is called with three arguments: the exception type, exception value, and traceback `(exc_type, exc_val, exc_tb)`. The context manager runs its cleanup code. If `__exit__` returns `True`, it tells Python "I have handled and squashed this exception," and execution continues harmlessly outside the `with` block. If it returns `False` or `None` (the default), the exception propagates up the call stack after cleanup.

**Q4: We have a generator streaming a massive AWS S3 file linearly. We realize we need to peek at the next item but not consume it, because we want to pass the intact rest of the stream to another function. How?**
> **Answer:** Normal iterators cannot peek ahead without consuming (`next(stream)` permanently pulls the item). The solution is either passing the `next()` value along manually, or using `itertools.tee()`, which splits a single iterable into two independent iterables, allowing you to peek at one while conserving the other. A simpler practical approach often used is writing a small wrapper class that caches the last pulled item.

---

[← Previous: Error Handling](06-error-handling.md) | [Back to Index](../README.md) | [Next: Concurrency & Parallelism →](08-concurrency.md)
