# 04. Data Structures & Collections — Production Deep Dive

> Big O notation matters. I've seen API endpoints drop from 400ms to 8ms simply by converting a `list` lookup to a `set` lookup. When writing code for data engineering and platform services, you must instinctively know the memory overhead and time complexities of Python's built-in structures.

---

## 🔍 Core Data Structures Complexity

You cannot build scalable systems without internalizing this table. 

| Operation | `list` | `dict` | `set` | Notes |
|-----------|--------|--------|-------|-------|
| Add Item | O(1)* | O(1)* | O(1)* | *Lists append O(1), insert(0) is O(n). Dict/Set resizing can trigger O(n) spikes. |
| Look Up (`in`) | **O(n)** | **O(1)** | **O(1)** | This is the #1 performance bug in junior level code. |
| Retrieve/Get | O(1) | O(1) | N/A | Indexing array vs hashing key. |
| Delete Item | O(n) | O(1) | O(1) | Removing from middle of array requires shifting. |

### The Power of Sets
Sets are backed by hashtables. They are exceptionally fast for comparisons, deduplications, and membership testing.

```python
# The bad way (List lookup in a loop is O(n^2) time)
banned_ips = ["10.0.0.1", "10.0.0.2", ...] # 100,000 items
for user_ip in traffic_logs:
    if user_ip in banned_ips:  # Scans the entire list linearly!
        block_user()

# The production way (O(n) time total)
banned_ips_set = set(["10.0.0.1", "10.0.0.2", ...]) 
for user_ip in traffic_logs:
    if user_ip in banned_ips_set: # Instant O(1) hash lookup!
        block_user()

# Instant set operations (C-level optimized)
common_ips = list(set(server1_ips) & set(server2_ips)) # Intersection
missing_ips = list(set(expected_nodes) - set(actual_nodes)) # Difference
```

---

## 🏭 Standard Library Collections module

Built-in dicts and lists are great, but the `collections` module contains highly optimized structures we use extensively in platform engineering.

### 1. `defaultdict` (Grouping Operations)
Eliminates `KeyError` edge cases when building aggregate dictionaries.

```python
from collections import defaultdict

log_entries = [("INFO", "msg1"), ("ERROR", "msg2"), ("INFO", "msg3")]

# Boring, error-prone way
logs_by_level = {}
for level, msg in log_entries:
    if level not in logs_by_level:
        logs_by_level[level] = []
    logs_by_level[level].append(msg)

# The DevOps standard way
logs_by_level = defaultdict(list)
for level, msg in log_entries:
    logs_by_level[level].append(msg)
```

### 2. `deque` (High-Performance Queues)
Python `list.pop(0)` is strictly O(n). If you are building a task queue or sliding window in Python, you must use a double-ended queue.

```python
from collections import deque

# SRE Sliding Window Rate Limiter
request_timestamps = deque(maxlen=100) # Automatically drops oldest when > 100

request_timestamps.append(current_time) # O(1)
oldest = request_timestamps[0]          # O(1)
```

### 3. `Counter` (Data Frequency)

```python
from collections import Counter

# Finding the most common IP triggering WAF rules
ip_bans = ["1.1.1.1", "2.2.2.2", "1.1.1.1", "8.8.8.8", "1.1.1.1"]
stats = Counter(ip_bans)

print(stats.most_common(1)) # [('1.1.1.1', 3)]
```

---

## 🤖 MLOps & LLMOps Application

### Memory Layouts: Struct of Arrays vs Array of Structs
When feeding data to Pandas or PyTorch, how you structure your Python collections directly dictates vectorization speeds.

```python
# Array of Structs (Row-based) - Natural to write, slow to process
# Caches poorly because memory is scattered
data_aos = [
    {"x": 1.0, "y": 2.0},
    {"x": 3.0, "y": 4.0}
]

# Struct of Arrays (Column-based) - MLOps standard
# Contiguous in memory, easily converted to Pandas/Numpy without overhead
data_soa = {
    "x": [1.0, 3.0],
    "y": [2.0, 4.0]
}
```

### Dict Views and Generators
When evaluating ML model metrics, dict size can balloon. Dict `.keys()`, `.values()`, and `.items()` return memory-efficient *view objects*, not instantiated lists (as they did in Python 2). 

```python
weights = {"layer1": 0.5, "layer2": -1.2, "layer3": 0.8}

# This does NOT copy the keys into an array, it iterates dynamically
for layer_name in weights.keys():  
    pass
```

---

## 🎯 Senior Engineer Interview Questions

**Q1: How handles Python dictionary hash collisions internally?**
> **Answer:** Python dicts use open addressing with "random" probing. When a hash collision happens (two keys compute to the same index array slot), Python generates a pseudo-random progression (based on the original hash) to jump to the next available slot. This is memory efficient compared to chaining (using linked lists at each index), but causes severe performance degradation if the table gets too full, which is why Python resizes dicts when they hit a 2/3 load factor.

**Q2: We are writing a custom Kubernetes controller in Python. We need to maintain an in-memory queue of Pod events to process. Should we use a `list` or a `deque`? Why?**
> **Answer:** We absolutely must use a `deque` (double-ended queue) from the `collections` module. In an event loop, we enqueue at the back and dequeue from the front (FIFO). In a standard `list`, `list.insert(0, item)` and `list.pop(0)` require shifting every single element in the memory array over by one index, an O(n) operation resulting in terrible latency under load. A `deque` uses a doubly-linked list under the hood, making appends and pops O(1) on both ends.

**Q3: Explain the difference between `.sort()` and `sorted()`.**
> **Answer:** `.sort()` is a method on the list object that sorts it in-place and returns `None`. It is memory efficient because it mutates the existing data. `sorted()` is a built-in function that takes any iterable, creates a brand new list, sorts it, and returns the new list, leaving the original data untouched. 

**Q4: You have an ML feature pipeline combining three dictionaries holding hundreds of thousands of attributes. What is the most compute/memory efficient way to combine them in Python 3.9+?**
> **Answer:** In Python 3.9+, you should use the union operator: `merged = dict1 | dict2 | dict3`. It is implemented in C-level code, is highly optimized, and reads perfectly cleanly. It resolves conflicts left-to-right (the rightmost dict takes precedence). Prior to 3.9, dictionary unpacking `merged = {**dict1, **dict2, **dict3}` was the standard optimized approach.

---

[← Previous: Object-Oriented Programming](03-oop.md) | [Back to Index](../README.md) | [Next: File I/O & Serialization →](05-file-io-serialization.md)
