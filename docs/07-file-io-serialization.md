# 07. File I/O & Serialization — JSON, Pickle & High-Performance Data

> "Disk I/O is one of the slowest parts of an application. An expert knows not just how to open a file, but how to use Buffering, Streams, and fast serialization formats like `Pickle` or `msgpack` to move gigabytes of data without locking the CPU or crashing the RAM."

---

## ❓ The 'Why' (High-Level)
Persistence is what makes software useful. Whether it's saving user settings or processing terabytes of logs, data must be written to and read from "Cold Storage" (Disk). A principal engineer understands that reading 1 byte at a time is 1,000x slower than reading in chunks, and that modern serialization (like Protobuf) can reduce network costs by 80%.

---

## 🌱 Module 1: The Basics (Junior) — Open, Read, Close
The entry-level way to handle files involves the `open()` function.

### 1. The Open/Close Cycle
- **`r`**: Read mode (Default).
- **`w`**: Write mode (Overwrites file).
- **`a`**: Append mode (Adds to the end).
```python
f = open("data.txt", "w")
f.write("Hello World")
f.close()
```

### 2. Reading Lines
Never use `.read()` on a file if you don't know its size. It will crash your computer if the file is massive. Instead, use a loop:
```python
for line in open("large_file.txt"):
    process(line)
```

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — Paths & JSON
Professional projects don't use string concatenation for file paths. They use objects.

### 1. Modern Paths with `pathlib`
`pathlib` handles the differences between Windows (`\`) and Linux (`/`) automatically.
```python
from pathlib import Path
log_file = Path("logs") / "today.log"
print(log_file.exists())
```

### 2. JSON Serialization
JSON is the standard format for Web APIs and config files.
```python
import json
data = {"id": 1, "status": "active"}

# Save to disk
with open("user.json", "w") as f:
    json.dump(data, f)
```

---

## 🌳 Module 3: Advanced Mechanics (Senior) — Buffering & Binary
Senior engineers look under the hood of I/O performance.

### 1. Buffering
By default, Python uses a **Buffer** in RAM. It doesn't write to the disk every time you call `write()`. It waits until the buffer is full (usually 4KB or 8KB) and then performs one "Flush" to the physical disk. This is drastically faster.

### 2. The `io` Module: BytesIO & StringIO
Sometimes you need to treat a string or a byte-string as if it were a file (e.g., to pass it to a function that only accepts file objects).
```python
import io
virtual_file = io.StringIO("This is a string-based file")
print(virtual_file.read())
```

---

## 🔥 Module 4: Principal Architect (Principal) — High-Performance Serialization
At the highest level, you choose the right **format** for speed and security.

### 1. The Serialization Trinity
- **JSON**: Human-readable, slow, no type safety.
- **Pickle**: Python-only, extremely fast, but **Dangerous** (loading a malicious pickle file can result in Remote Code Execution).
- **MessagePack/Protobuf**: Binary, extremely small, fast, and secure.

### 2. Memory Mapping (`mmap`)
For files larger than your RAM, you can use `mmap` to "Map" the file directly into your process's address space. The OS only loads the parts of the file you are actually reading, giving you "Instant" random access to a 100GB file.

---

## 🏗️ Case Study: Processing a 50GB Log File
A cybersecurity company needed to scan 50GB of daily firewall logs for specific IP addresses.
- **The Junior Approach**: `with open(file) as f: lines = f.readlines()`. (Crashed immediately due to Out-Of-Memory).
- **The Principal Approach**: Used **`mmap`** to scan the data without loading it all into memory and used **Generators** to stream the matches to a result file.
- **Result**: The scan finished in 4 minutes using only 50MB of RAM.

---

## ⚡ Anti-Patterns & Expert Traps

### 1. The Insecure `pickle.load()`
Never use `pickle.load()` on data that comes from a user/external API. An attacker can craft a pickle that executes `rm -rf /` when loaded. **Expert fix**: Use `json` or `yaml` for untrusted data.

### 2. Manual `f.close()`
Always use a Context Manager (`with open()`). If your code crashes before `f.close()`, the file handle stays open, eventually leading to "Too many open files" errors.

---

## 🎯 Top 20 Principal Interview Questions (File I/O & Serialization)

1. **Q: What is the difference between `read()`, `readline()`, and `readlines()`?**
   - **Answer**: `read()` loads the **Entire File** into memory. `readline()` reads only the **Next Single Line**. `readlines()` reads the entire file but splits it into a **List of Lines**. Always prefer manual line iteration for large files.
2. **Q: Why is it important to use 'Context Managers' (`with` statement) for files?**
   - **Answer**: Because they guarantee that the file will be closed automatically, even if an exception occurs inside the block. This prevents **Resource Leaks** and ensures the data buffer is flushed correctly.
3. **Q: What is the difference between 'Text Mode' (`t`) and 'Binary Mode' (`b`)?**
   - **Answer**: Text mode automatically handles **Encoding** (like UTF-8) and newline characters (`\n` vs `\r\n`). Binary mode returns or writes the raw bytes without any translation.
4. **Q: Explain 'Buffering' in Python's file I/O.**
   - **Answer**: Buffering is a performance optimization where Python collects data in RAM before performing a single, large read or write to the physical disk, which is a relatively slow operation.
5. **Q: What is `pathlib` and why is it preferred over `os.path`?**
   - **Answer**: `pathlib` provides an **Object-Oriented** approach to path manipulation. It's more readable, more secure (avoids accidental string errors), and much better for cross-platform compatibility.
6. **Q: What is the risk of using `pickle.load()`?**
   - **Answer**: `Pickle` is not secure. A malicious pickle file can execute **Arbitrary Code** on your machine the moment it is loaded. Only use it for trusted, internal data.
7. **Q: How can you read a specific part of a file (e.g., the last 100 bytes)?**
   - **Answer**: Using the `f.seek(offset, from_what)` method to move the file pointer and then calling `f.read(100)`.
8. **Q: What is 'JSON Serialization'?**
   - **Answer**: The process of converting a Python object (like a dictionary) into a **JSON string** so it can be saved to disk or sent over a network.
9. **Q: Explain the difference between `json.dump()` and `json.dumps()`.**
   - **Answer**: `json.dump()` (no 's') writes data directly to a **File object**. `json.dumps()` (with 's') returns the data as a **String**.
10. **Q: What is 'CSV' and how does Python handle it?**
    - **Answer**: **Comma Separated Values**. The built-in `csv` module handles the complex rules of delimiters, quoting, and newlines that manual string splitting usually fails at.
11. **Q: How do you handle encoding errors (like `UnicodeDecodeError`)?**
    - **Answer**: By specifying the `encoding` parameter in `open()` (e.g., `utf-8`) and potentially using the `errors` parameter (e.g., `ignore` or `replace`).
12. **Q: What is `io.BytesIO`?**
    - **Answer**: A class that allows you to treat a byte-string as a **File-like object**. It's useful for testing or for libraries that require a file input when you only have the data in memory.
13. **Q: What is 'mmap' (Memory Mapping)?**
    - **Answer**: A technique to "Map" a file directly into a process's virtual memory address space. It allows for extremely fast, low-RAM I/O on massive files.
14. **Q: How do you flush a file's buffer manually?**
    - **Answer**: By calling `f.flush()`. This forces any data in the RAM buffer to be written to the OS's disk buffer.
15. **Q: What is the difference between `os.remove()` and `shutil.rmtree()`?**
    - **Answer**: `os.remove()` deletes a single file. `shutil.rmtree()` recursively deletes an entire directory and all its contents.
16. **Q: What is 'YAML' and why is it often used for configuration files?**
    - **Answer**: **Yet Another Markup Language**. It's more human-readable than JSON and supports advanced features like comments and anchors, but requires an external library (like PyYAML).
17. **Q: How can you count the number of lines in a 10GB file without crashing?**
    - **Answer**: `sum(1 for _ in open(file))`. This iterates through the file without loading more than one line at a time into memory.
18. **Q: What is `shutil.copy` vs `shutil.copy2`?**
    - **Answer**: Both copy the file content, but `copy2` also attempts to preserve the file's **Metadata** (like creation and modification timestamps).
19. **Q: What is 'Atomic Writing'?**
    - **Answer**: Writing your data to a temporary file first and then **Renaming** it to the final destination. This ensures that even if the computer crashes mid-write, the original file is never corrupted.
20. **Q: What is the `sys.stdin` and `sys.stdout`?**
    - **Answer**: They are the standard input and output streams. In Python, they are treated as **File-like objects**, so you can read from `stdin` just like you read from a file.

---

[Previous: Error Handling](06-error-handling.md) | [Next: Object-Oriented Programming →](08-object-oriented-programming.md)
