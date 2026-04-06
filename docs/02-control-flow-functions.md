# 02. Control Flow & Functions — Production Deep Dive

> Writing a loop is easy. Writing a loop that survives processing 10 million Kafka messages without memory leaks or silent failures is engineering. The way we structure functions and control flow dictates the maintainability of our platform codebase.

---

## 🔍 Core Flow Concepts Revisited

### The Truthiness Trap
Python evaluates objects in boolean contexts implicitly. Empty lists, dicts, strings, 0, and `None` evaluate to `False`. Relying on implicit truthiness is clean but dangerous in configuration parsing.

```python
# Dangerous in IaC/DevOps:
config = get_user_config() # Returns {}
if not config:
    use_defaults() # What if the user explicitly WANTED an empty config?

# Explicit is better than implicit (PEP 20):
if config is None:
    use_defaults()
```

### Unpacking & Wildcard Assignments (`*`)
We deal with variable-length API responses constantly. Iterating by index is an anti-pattern. Use structural unpacking.

```python
aws_vpc_data = ["vpc-12345", "us-east-1", "10.0.0.0/16", "available", "prod-vpc"]

# Beautiful extraction
vpc_id, region, *network_specs, name = aws_vpc_data

print(vpc_id) # vpc-12345
print(network_specs) # ['10.0.0.0/16', 'available']
```

---

## 🏭 Function Scoping & Execution Patterns

### First-Class Functions & Higher-Order Patterns
In Python, functions are objects. You can pass them as arguments, return them, and store them in dicts. We use this extensively to avoid massive `if-elif` chains, a pattern known as **Dispatcher Dictionaries**.

```python
# Instead of this 50-line nightmare:
def handle_event(event_type, payload):
    if event_type == "EC2_START":
        process_ec2_start(payload)
    elif event_type == "S3_UPLOAD":
        process_s3_upload(payload)
    # ... 20 more elifs

# Do this (O(1) lookup, highly testable):
def process_ec2_start(payload): pass
def process_s3_upload(payload): pass

EVENT_HANDLERS = {
    "EC2_START": process_ec2_start,
    "S3_UPLOAD": process_s3_upload,
}

def handle_event(event_type, payload):
    handler = EVENT_HANDLERS.get(event_type)
    if not handler:
        raise ValueError(f"Unknown event type: {event_type}")
    handler(payload)
```

### Closures and Late Binding (The `lambda` Bug)
A closure remembers the variables from its enclosing scope. But in Python, closures are *late-binding*. This breaks a lot of dynamic script generation.

```python
# The Bug
callbacks = []
for i in range(3):
    callbacks.append(lambda: f"Node {i}")

print([c() for c in callbacks]) 
# Expected: ['Node 0', 'Node 1', 'Node 2']
# Actual:   ['Node 2', 'Node 2', 'Node 2'] 

# The Fix (Early binding via default argument)
callbacks = []
for i in range(3):
    callbacks.append(lambda i=i: f"Node {i}")
```

---

## 🔧 DevOps & Cloud Perspectives

### Subprocess Execution Flow
When wrapping bash commands (kubectl, terraform) in Python, dealing with standard out and exit codes is where scripts usually fail silently.

```python
import subprocess
import logging

def run_kubectl(cmd: list) -> str:
    """Safe subprocess wrapper for SRE tooling"""
    try:
        # capture_output=True, check=True prevents silent failures
        result = subprocess.run(
            ["kubectl"] + cmd, 
            capture_output=True, 
            text=True, 
            check=True,
            timeout=30 # Prevent hanging orchestrations
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed (exit {e.returncode}): {e.stderr}")
        raise
    except subprocess.TimeoutExpired as e:
        logging.error(f"Command timed out: {e}")
        raise
```

---

## 🤖 MLOps / AI Perspective

### \*args and \*\*kwargs in Model Frameworks
Deep learning libraries (PyTorch/HuggingFace) use `kwargs` to pass configurations through multiple layers of abstraction.

```python
from transformers import AutoModelForCausalLM

def load_llm(model_id, **kwargs):
    # Base sensible defaults 
    config = {
        "device_map": "auto",
        "torch_dtype": "auto",
    }
    # Update with passed kwargs, allowing users to override if needed
    config.update(kwargs)
    
    return AutoModelForCausalLM.from_pretrained(model_id, **config)

# Using our wrapper
# Overrides device_map but keeps torch_dtype
model = load_llm("meta-llama/Llama-2-7b", device_map="cuda:0", load_in_8bit=True)
```

---

## 🎯 Senior Engineer Interview Questions

**Q1: What's the difference between `yield` and `return`? When would you use one over the other in data pipelines?**
> **Answer:** `return` exits the function entirely and sends back a value, destroying the function's local state. `yield` turns the function into a generator, pausing execution, returning a value, and keeping the local state intact until `next()` is called again. In data pipelines (like reading large S3 CSVs), I use `yield` to stream data row-by-row into memory rather than `return`ing a massive list that would trigger an OOM kill.

**Q2: We need to write a function that retries a flaky API call 3 times. How would you structure this cleanly?**
> **Answer:** Instead of polluting the business logic with retry loops, I would write a decorator. The decorator would wrap the function, implement a `while` loop or `for` loop over attempts, catch specific `RetryableExceptions` (like HTTP 503s), apply exponential backoff using `time.sleep()`, and finally raise the error if out of retries. Better yet, in production, I'd rely on an existing library like `tenacity` to handle this.

**Q3: Is Python pass-by-value or pass-by-reference? How does this affect passing large PyTorch tensors into functions?**
> **Answer:** Python is technically "pass-by-object-reference" or "pass-by-assignment". It doesn't pass the variable box, it passes a reference to the underlying memory object. Because a PyTorch tensor is mutable, passing it into a function does not copy the tensor data; you are acting on the exact same multi-gigabyte block in GPU/CPU memory. Modifying it in the function modifies it everywhere. If you need a clean version, you must explicitly call `.clone()`.

**Q4: Explain the risk of using recursive functions in Python vs languages like Go/C++.**
> **Answer:** Python lacks "Tail Call Optimization" (TCO). In languages with TCO, recursive calls that are the last operation in a function reuse the current stack frame. Python creates a new stack frame for every recursive call. This means a recursion depth of just ~1000 will result in a `RecursionError` and crash the program. Therefore, in Python, we avoid deep recursion entirely and refactor algorithms (like tree traversals) into iterative approaches using manual stacks or queues.

---

[← Previous: Data Types](01-data-types-variables.md) | [Back to Index](../README.md) | [Next: Object-Oriented Programming →](03-oop.md)
