# 05. File I/O & Serialization — Production Deep Dive

> If processing a 1GB file consumes 2GB of RAM, your architecture is broken. In data engineering and ML platforms, how we serialize and load data dictates system throughput. We're stepping past basic `open('file.txt')` into high-performance streaming, state persisting, and binary protocols.

---

## 🔍 Core I/O Operations

### Context Managers (`with`)
Never manually call `.close()`. File descriptors are limited OS resources. In auto-scaling environments, leaking file handlers rapidly leads to `Too many open files` errors, bringing down entire nodes.

```python
# The DevOps standard (guarantees closure even on Exception)
import pathlib

# pathlib is objectively superior to os.path
logs_dir = pathlib.Path('/var/log/app')
for log_file in logs_dir.glob('*.log'):
    with log_file.open('r') as f:
        # Processing happens here
        pass 
```

### Buffer Sizes and Memory Leaks
`f.read()` loads the entire file into memory. Iterating over the file object `for line in f:` buffers text line-by-line using a hidden internal buffer. 

```python
# SRE parsing 50GB access logs
with open("vpc_flow_logs.csv", "r", buffering=8192) as f:
    for line in f: # Reads chunk by chunk, keeping memory flat
        process_log(line) 
```

---

## 🏭 Serialization Formats (JSON, YAML, Pickle)

### JSON (JavaScript Object Notation)
The lingua franca of APIs. 

*   **Pitfall:** `json.load()` requires full structural reading before yielding memory.
*   **Fix:** For large streaming APIs, use `ijson`.

```python
import json

data = {"instance": "i-1234a", "region": "us-east-1"}
# Serialize to string
json_str = json.dumps(data)

# Deserialize from string
obj = json.loads(json_str)
```

### YAML (YAML Ain't Markup Language)
Kubernetes and CI/CD config heart. 

*   **Warning:** NEVER use `yaml.load(file)`. It can execute arbitrary Python functions (RCE vulnerability). 
*   **Fix:** **Always** use `yaml.safe_load()`.

```python
import yaml

with open('pod-spec.yaml', 'r') as f:
    # safe_load ignores Python-specific tags, stopping code execution
    k8s_spec = yaml.safe_load(f) 
```

### Pickle (Python Binary Serialization)
Used for saving models. 

*   **Warning:** Unpickling is essentially executing a virtual machine. If an attacker tampers with a `.pkl` file, loading it grants them immediate root execution context. NEVER unpickle untrusted data.

```python
import pickle

model_weights = {"conv1": [0.1, 0.4], "layer2": [0.8, -0.1]}

# Save model (binary 'wb')
with open("weights.pkl", "wb") as f:
    pickle.dump(model_weights, f)
```

---

## 🤖 MLOps & LLMOps Application

### The Problem with Python Pickles in ML
The ML ecosystem (specifically PyTorch `torch.save()`) historically relied heavily on Pickle. This poses a massive security risk when downloading weights from platforms like HuggingFace.

**The modern solution:** `safetensors`.

It is a zero-copy, memory-mapped format that prevents remote code execution and loads instantly.

```python
from safetensors.torch import save_file, load_file
import torch

tensors = {
    "embedding": torch.zeros((10, 10)),
    "attention": torch.zeros((10, 10))
}

# Fast, secure save
save_file(tensors, "model.safetensors")

# Secure load (prevents RCE attacks from malicious model files)
loaded = load_file("model.safetensors")
```

### Parquet vs CSV (Data Engineering)
Pandas loading CSVs is a massive bottleneck. CSVs carry no typing information (everything is a string), requiring slow regex-based inference. **Parquet** is a columnar binary format. 

*   Parquet is strongly typed.
*   Parquet uses Snappy/Gzip compression internally.
*   Parquet supports partition pruning (only reading required columns).

```python
import pandas as pd

# Terribly slow + high memory
df = pd.read_csv("training_data.csv") 

# Write to parquet
df.to_parquet("training_data.parquet", engine='pyarrow')

# Read specific columns 100x faster 
df = pd.read_parquet("training_data.parquet", columns=["user_id", "click_prob"])
```

---

## 🎯 Senior Engineer Interview Questions

**Q1: Why should you avoid `yaml.load()` and what are the security implications?**
> **Answer:** `yaml.load()` in the standard PyYAML library evaluates YAML tags. If an attacker submits a payload like `!!python/object/apply:os.system ["whoami"]`, the loader will execute the OS command during deserialization, resulting in Remote Code Execution (RCE). To prevent this, we must exclusively use `yaml.safe_load()` which restricts parsing to basic YAML data types.

**Q2: We need to design an API that accepts a 5GB video upload, processes it, and uploads to S3. How do you handle the temporary file I/O in a container without causing ephemeral storage issues?**
> **Answer:** I would not touch the container's disk at all. I would use the `tempfile.SpooledTemporaryFile` module, which keeps the file heavily buffered in RAM up to a specified size before silently spilling to disk. Alternatively, I would pipe the incoming HTTP request stream directly to the `boto3` `upload_fileobj()` method as a multipart upload, establishing a memory-efficient bypass that streams data straight to S3 without persisting locally.

**Q3: Contrast `.csv` and `.parquet` in the context of an MLOps pipeline.**
> **Answer:** CSV is row-based, uncompressed, and untyped text. Pandas has to guess types upon loading, which is incredibly CPU-intensive. Parquet is an open-source, columnar binary format. Because it is columnar, we can load just specific columns without loading the entire dataset into memory. It is strongly typed, so memory mapping is immediate, and heavily compressed, reducing S3 transfer costs significantly.

**Q4: A PyTorch model trained in dev won't load in production because of a "ModuleNotFoundError" during `torch.load()`. Why did this happen?**
> **Answer:** Standard `torch.load` relies on Python's `pickle`. Pickle does not serialize the actual class code—it only serializes the data (state) and a *string reference* to the original class path. If the production environment refactored the module paths, Pickle can't find the class template to map the data to. This is why in production ML, we only save state dicts (`model.load_state_dict(torch.load(path))`), or use cross-platform standards like ONNX or Safetensors.

---

[← Previous: Data Structures](04-data-structures.md) | [Back to Index](../README.md) | [Next: Error Handling & Debugging →](06-error-handling.md)
