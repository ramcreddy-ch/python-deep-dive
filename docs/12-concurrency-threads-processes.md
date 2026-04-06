# 12. Concurrency: Threads & Processes — GIL, Parallelism & Safety

> "Writing code that runs on one core is easy. Writing code that runs safely on 64 cores is what separates a developer from a principal engineer. You must understand the GIL, Shared Memory, and the fundamental differences between I/O-bound and CPU-bound concurrency."

---

## ❓ The 'Why' (High-Level)
Modern servers have many CPU cores. If your Python script only uses one, you are paying for 95% of a server you aren't using. **Concurrency** allows your code to do multiple things at once (e.g., handling 100 API requests), and **Parallelism** allows it to do things at the *exact same time* on different cores. A principal engineer chooses the right tool: **Threads** for waiting (I/O) and **Processes** for calculating (CPU).

---

## 🌱 Module 1: The Basics (Junior) — Threading
A **Thread** is like a separate worker inside your program.

### 1. Basic Threading
Threads share the same memory, making them very "Lightweight."
```python
import threading

def worker(num):
    print(f"Worker {num} starting")

t = threading.Thread(target=worker, args=(1,))
t.start()
t.join()  # Wait for the thread to finish!
```

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — Multi-Processing
Because of Python's **GIL** (Global Interpreter Lock), threads cannot run on multiple CPU cores at once. To get true speed for heavy calculations, you must use **Processes**.

### 1. `multiprocessing`
Each process has its **own memory** and its **own Python interpreter**.
```python
import multiprocessing

def heavy_math(n): return n * n

p = multiprocessing.Process(target=heavy_math, args=(10,))
p.start()
```

### 2. Pooled Execution (`concurrent.futures`)
Professional code uses "Pools" to manage workers automatically.
```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(my_function, data_list))
```

---

## 🌳 Module 3: Advanced Mechanics (Senior) — The GIL & Safety
Senior engineers understand the "Single Thread" limit of Python.

### 1. The Global Interpreter Lock (GIL)
The GIL is a mutex that prevents multiple threads from executing Python bytecode at the same time. This is necessary because CPython's memory management is NOT thread-safe.
- **Impact**: Multi-threading in Python is only fast for **I/O-bound** tasks (waiting for network/disk).

### 2. Thread Safety (Locks)
Because threads share memory, they can overwrite each other's data (a **Race Condition**).
```python
lock = threading.Lock()
with lock:
    shared_counter += 1  # Only one thread can do this at once!
```

---

## 🔥 Module 4: Principal Architect (Principal) — GIL Bypassing & IPC
At the highest level, you scale your application across the entire server cluster.

### 1. Releasing the GIL
Libraries like **NumPy** or **Pandas** are written in C. When they do heavy math, they "Release the GIL," allowing true multi-core parallelism while still being called from a single Python script.

### 2. Shared Memory & IPC
Sharing data between processes is "Expensive" because it must be serialized (pickled).
- **Principal Choice**: Use `multiprocessing.shared_memory` to allow two processes to look at the same block of RAM directly without copying it.

---

## 🏗️ Case Study: The High-Speed Image Resizer
A photography platform was resizing 10,000 high-res images per minute.
- **The Junior Approach**: Using `threading` (Wait—resizing is CPU-bound!). The code actually ran **slower** than single-threaded code due to GIL contention.
- **The Principal Approach**: Switched to a **`ProcessPoolExecutor`** and used **Shared Memory** to avoid copying large raw image bytes between processes.
- **Result**: Resizing time dropped from 15 minutes to **2 minutes** on a 16-core server.

---

## ⚡ Anti-Patterns & Expert Traps

### 1. Threads for CPU Tasks
If your logic is math-heavy (Encryption, Compression, Image processing), **DO NOT USE THREADS**. You will only get the performance of a single core. Use `multiprocessing`.

### 2. "Zombie" Processes
If you start a process but don't call `.join()`, it can stay in the system as a "Zombie" long after your script is done. Always use a Context Manager (`with`) for pools.

---

## 🎯 Top 20 Principal Interview Questions (Concurrency)

1. **Q: What is the 'GIL' (Global Interpreter Lock)?**
   - **Answer**: It is a mutex that allows only one thread to execute Python bytecode at a time. It's necessary because CPython's memory management is not thread-safe.
2. **Q: What is the difference between a 'Thread' and a 'Process'?**
   - **Answer**: **Threads** share the same memory space (Lightweight). **Processes** have separate memory space and separate interpreters (Heavyweight, but allows for true parallelism).
3. **Q: When should you use Multi-threading instead of Multi-processing?**
   - **Answer**: Use **Multi-threading** for **I/O-bound** tasks (network calls, disk access). Use **Multi-processing** for **CPU-bound** tasks (heavy math, image processing).
4. **Q: What is a 'Race Condition'?**
   - **Answer**: Not a physical contest, but a bug where two threads try to modify the same shared data simultaneously, leading to unpredictable and incorrect results.
5. **Q: Explain 'Thread Safety' and how to achieve it.**
   - **Answer**: Thread safety means code that functions correctly when used by multiple threads at once. It is achieved using **Locks**, **RLocks**, **Semaphores**, or **Thread-Safe Data Structures** (like `queue.Queue`).
6. **Q: What is a 'Deadlock'?**
   - **Answer**: A situation where two threads are each waiting for the other to release a lock, causing both to be stuck forever.
7. **Q: What is the purpose of `target.join()`?**
   - **Answer**: It tells the main program to **Stop and Wait** for that specific thread or process to finish before continuing.
8. **Q: What is a 'Daemon Thread'?**
   - **Answer**: A background thread that doesn't prevent the main program from exiting. When the main program ends, all daemon threads are killed immediately.
9. **Q: Explain the `concurrent.futures` module.**
   - **Answer**: A modern and simplified API for managing pools of threads or processes. It provides `ThreadPoolExecutor` and `ProcessPoolExecutor`.
10. **Q: What is 'Context Switching'?**
    - **Answer**: The process of the CPU saving the state of one thread and loading the state of another. Frequent context switching (with too many threads) can make an application slower.
11. **Q: How does `multiprocessing.Queue` differ from `queue.Queue`?**
    - **Answer**: `queue.Queue` is only for threads (shared memory). `multiprocessing.Queue` is designed to share data between **Processes** via serialization (pickling).
12. **Q: What is an 'RLock' (Re-entrant Lock)?**
    - **Answer**: A lock that can be acquired **multiple times** by the same thread without causing a deadlock.
13. **Q: Why don't standard Python threads speed up a CPU-intensive loop?**
    - **Answer**: Because of the **GIL**. Even if you have 10 threads, only one can be executing bytecode at any given millisecond.
14. **Q: What is 'Shared Memory' in Multi-processing?**
    - **Answer**: A technique where a block of RAM is made available to multiple processes simultaneously, avoiding the high cost of copying data between them.
15. **Q: Explain 'CPU Affinity'.**
    - **Answer**: Binding a specific process or thread to a specific CPU core to improve performance (common in high-performance computing).
16. **Q: What is the purpose of a 'Semaphore'?**
    - **Answer**: A synchronization tool that allows a fixed number of threads (e.g., 5) to access a resource at once, rather than just one (Lock).
17. **Q: What is 'IPC' (Inter-Process Communication)?**
    - **Answer**: The mechanism that allows processes to communicate and synchronize their actions (e.g., Pipes, Queues, Shared Memory).
18. **Q: Can you 'Kill' a thread in Python?**
    - **Answer**: **No**. Python's `threading` module does not provide a way to forcefully kill a thread (it's unsafe). You must signal the thread to exit voluntarily.
19. **Q: What is the 'Pool' pattern?**
    - **Answer**: Pre-creating a fixed number of workers (threads/processes) and "Feeding" them tasks, rather than creating a new thread for every tiny task.
20. **Q: What is 'GIL Contention'?**
    - **Answer**: When multiple threads are constantly fighting to acquire the GIL, leading to significant performance degradation even if the threads aren't doing much work.

---

[Previous: Generators](11-generators-iterators.md) | [Next: AsyncIO →](13-asyncio-concurrency.md)
