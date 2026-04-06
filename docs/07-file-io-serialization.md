# 07. File I/O & Serialization — JSON, Pickle & High-Performance Data

> "Disk I/O is one of the slowest parts of an application. An expert knows not just how to open a file, but how to use Buffering, Streams, and fast serialization formats like `Pickle` and `Joblib` to handle gigabytes of data efficiently."

---

## 🌱 The Basics: Reading & Writing Text
The entry-level way to handle files. Use the `with` statement (Context Manager) to ensure files are closed automatically.

```python
# 1. Writing a file
with open("data.txt", "w") as f:
    f.write("Hello Python!")

# 2. Reading a file line-by-line
with open("data.txt", "r") as f:
    for line in f:
        print(line.strip())
```

---

## 🌿 Intermediate: JSON & Serialization
Serialization is the process of turning a Python object (like a dictionary) into a string or bytes that can be saved to disk or sent over a network.

**Real Use (API/Config)**:
Most modern configurations and APIs use **JSON**.

```python
import json

user = {"id": 101, "name": "Ramchandra", "roles": ["Admin", "SRE"]}

# Write to file (Serialize)
with open("user.json", "w") as f:
    json.dump(user, f, indent=4)

# Read from file (Deserialize)
with open("user.json", "r") as f:
    data = json.load(f)
```

---

## 🌳 Advanced: Binary Serialization (Pickle & Joblib)
JSON only supports basic types (strings, numbers, lists). **Pickle** is Python's native binary format that can save almost **any** object, including complex classes and functions.

**Real Use (MLOps)**:
Saving a trained machine learning model. For large NumPy arrays, `joblib` is faster than `pickle`.

```python
import pickle
import joblib

# Model object
model = {"weights": [0.1, 0.5, 0.9], "type": "LinearRegression"}

# 1. Standard approach
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

# 2. High-performance MLOps approach
joblib.dump(model, "model_v2.jbl")
```

---

## 🔥 Expert: Streaming & Buffering
For principal-level engineering, you cannot load a 50GB log file into RAM. You must use **Generators** and **Buffers**.

### 1. Chunked Reading
Process data 10,000 lines at a time to keep memory usage under 100MB.

```python
def process_large_log(file_path):
    """
    Expert Pattern: Streamed Reading. 
    Demonstrates: Memory-safe I/O for massive data.
    """
    with open(file_path, "r", buffering=1024*1024) as f: # 1MB buffer
        while True:
            chunk = f.read(10000) # Read in blocks
            if not chunk:
                break
            # Process chunk...
```

---

## 🎯 Top 20 Principal Interview Questions (File I/O & Serialization)

1. **Q: Why is the `with` statement used for file handling?**
   - **Answer**: It is a Context Manager that guaranteed the file is **closed** appropriately, even if your code crashes. This prevents memory leaks and file lock errors on the OS level.
2. **Q: What is the difference between `pickle.dump()` and `pickle.dumps()`?**
   - **Answer**: `dump()` writes directly to a **file** object; `dumps()` (Dump String) returns the **bytes** of the serialized object directly in memory.
3. **Q: Why is `Pickle` considered a security risk?**
   - **Answer**: `pickle.load()` can execute arbitrary code stored in the file. If an attacker gives you a malicious pickle file, they can run commands on your machine the moment you open it. Never unpickle from untrusted sources.
4. **Q: How do you read a 50GB file on a machine with 16GB RAM?**
   - **Answer**: Using a **Generator** or **Chunked Reading**. Never use `.read()` or `.readlines()`, as they load the whole file into RAM. Iterate through the file object directly: `for line in f:`.
5. **Q: What is 'JSON Serialization' and what are its limitations?**
   - **Answer**: It converts a Python dict/list into a string. Limitations: It only supports basic types (strings, numbers, bools, lists, dicts). It **cannot** handle custom classes, dates, or complex objects without a custom encoder.
6. **Q: What is the difference between `r` and `rb` modes in `open()`?**
   - **Answer**: `r` is for **Text** (string). `rb` is for **Binary** (bytes). Binary is required for images, models, and serialized files like Pickle.
7. **Q: What is 'Buffering' and how does it impact performance?**
   - **Answer**: It is the practice of reading data into a small RAM block before processing it. Larger buffers (e.g., 1MB) reduce the number of slow calls to the actual hard drive, making I/O much faster.
8. **Q: How does `utf-8` encoding differ from `ascii`?**
   - **Answer**: `ascii` only supports basic English characters (7 bits). `utf-8` is a variable-length encoding that supports **Every language/emoji** in the world. It is the modern standard for production.
9. **Q: What is the purpose of `f.seek()` and `f.tell()`?**
   - **Answer**: `tell()` returns the current position of the pointer in the file. `seek(offset)` moves that pointer to a specific location (useful for random access to large files).
10. **Q: Why is `joblib` preferred over `pickle` in MLOps?**
    - **Answer**: `joblib` is optimized for large **NumPy arrays** and handles multiple processes better, making it the standard for saving ML models.
11. **Q: How do you handle writing to a file that is currently being read by another process?**
    - **Answer**: use a **File Lock** (via the `portalocker` or `fcntl` libraries) to ensure only one process can write at a time, preventing data corruption.
12. **Q: What is the difference between `json.load()` and `json.loads()`?**
    - **Answer**: `load()` reads from a **File**. `loads()` reads from a **String**.
13. **Q: What is a 'Path-like Object' in Python?**
    - **Answer**: An object representing a system path, like a standard string or the modern `pathlib.Path` object. `pathlib` is preferred in senior engineering because it is cross-platform.
14. **Q: How do you append text to an existing file without deleting it?**
    - **Answer**: Use the `"a"` (Append) mode in `open()`.
15. **Q: What is the purpose of `shutil` module?**
    - **Answer**: High-level file operations like **Copying, Moving, and Deleting** entire directories and file trees.
16. **Q: How do you securely delete a sensitive file in Python?**
    - **Answer**: Overwrite the file with random bits (`"wb"`) before deleting it to ensure it cannot be easily recovered from the disk.
17. **Q: What is 'End-of-Line' (EOL) character and how does Python handle it across OS?**
    - **Answer**: Windows uses `\r\n`, while Linux uses `\n`. Python's `open()` uses **Universal Newlines** (`newline=None`) to automatically convert these to `\n` for consistent processing.
18. **Q: What happens if you try to write to a read-only file?**
    - **Answer**: It raises a `PermissionError`.
19. **Q: What is the `tempfile` module used for?**
    - **Answer**: Creating temporary files and directories that are automatically deleted once the script finishes or the file is closed.
20. **Q: How do you ensure all data is actually written to disk before closing?**
    - **Answer**: Python buffers writes in RAM. To force an immediate write to disk, use `f.flush()` followed by `os.fsync(f.fileno())`.

---

[← Previous: Error Handling](../Level-1/06-error-handling.md) | [Next: OOP →](08-object-oriented-programming.md)
