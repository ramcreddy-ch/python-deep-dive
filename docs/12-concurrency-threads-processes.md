# 12. Concurrency: Threads & Processes — GIL, Parallelism & Safety

> "Writing code that runs on one core is easy. Writing code that runs safely on 64 cores is what separates a developer from a principal engineer. You must understand the GIL, Shared Memory, and the fundamental trade-off between Threads and Processes."

---

## 🌱 The Basics: Threading
A **Thread** is a "Lightweight" unit of execution that lives inside your main process. Threads share the same memory.

- **Best for**: **I/O-Bound** tasks (Reading from a disk, waiting for a network API).

```python
import threading
import time

def slow_io_task(name):
    print(f"Task {name} starting...")
    time.sleep(2) # Simulate network wait
    print(f"Task {name} finished.")

# Run 2 tasks at once
t1 = threading.Thread(target=slow_io_task, args=("Net-A",))
t2 = threading.Thread(target=slow_io_task, args=("Net-B",))

t1.start(); t2.start()
t1.join(); t2.join() # Wait for both to finish
```

---

## 🌿 Intermediate: Multiprocessing
A **Process** is an independent unit of execution with its own memory. It cannot see the variables of other processes.

- **Best for**: **CPU-Bound** tasks (Heavy math, image processing, data transformation).
- **The GIL Bypass**: Each process has its own **GIL** (Global Interpreter Lock), allowing you to use 100% of multiple CPU cores.

```python
from multiprocessing import Process

def compute_heavy_task(n):
    # Heavy math here...
    return n * n

# p = Process(target=compute_heavy_task, args=(100,))
# p.start(); p.join()
```

---

## 🌳 Advanced: Thread Safety & Locks
When multiple threads try to change the same global variable at the exact same time, you get a **Race Condition**. 

**Real Use (Platform/FinTech)**:
A counter or a bank balance that is accessed by multiple background threads.

```python
import threading

balance = 0
lock = threading.Lock() # The 'Safety Key'

def update_balance(amount):
    """
    Expert Pattern: Thread Safety. 
    Demonstrates: Preventing Race Conditions.
    """
    global balance
    with lock: # Only one thread can enter this block at a time
        balance += amount
```

---

## 🔥 Expert: Concurrent.Futures (The Pool Pattern)
Principal engineers use **Pools** to manage hundreds of tasks without creating hundreds of threads/processes manually.

```python
from concurrent.futures import ThreadPoolExecutor

def fetch_data(url):
    return f"Data from {url}"

urls = ["api.v1.com", "api.v2.com", "api.v3.com"]

# Expert Pattern: Executor Service. 
# 1. Spawns 10 workers in a pool.
# 2. Automatically distributes work.
with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(fetch_data, urls))
```

---

## 🎯 Top 20 Principal Interview Questions (Concurrency)

1. **Q: What is the GIL (Global Interpreter Lock)?**
   - **Answer**: It is a 'Mutex' (a lock) that allows only one thread to execute Python bytecode at a time. This ensures 'Thread-Safety' for CPython's memory management (Reference Counting). 
2. **Q: Threads vs. Processes — when to use which?**
   - **Answer**: **Threads** for **I/O-Bound** (waiting for data). **Processes** for **CPU-Bound** (crunching data).
3. **Q: What is a 'Race Condition'?**
   - **Answer**: When the outcome of an application depends on the unpredictable sequence or timing of threads. Example: Two threads incrementing a counter simultaneously might result in +1 instead of +2.
4. **Q: How does `threading.Lock()` solve race conditions?**
   - **Answer**: It acts as a "Baton." A thread must 'Acquire' the lock before it can proceed. Any other thread that tries to acquire it will 'Block' (wait) until the first thread 'Releases' it.
5. **Q: What is a 'Deadlock'?**
   - **Answer**: When two threads are waiting for each other to release a lock, causing the entire application to freeze forever. 
6. **Q: What is the `multiprocessing.Queue` used for?**
   - **Answer**: Since processes don't share memory, you use a **Queue** to safely send data (messages) between them.
7. **Q: What is the difference between `threading` and `concurrent.futures`?**
   - **Answer**: `threading` is low-level manual management. `concurrent.futures` is a high-level abstraction that use **Pools** to automate task distribution and result gathering.
8. **Q: What is a 'Daemon' thread?**
   - **Answer**: A thread that runs in the background. If all non-daemon threads finish, the Python program will exit even if a daemon thread is still running.
9. **Q: How can you bypass the GIL for heavy math without using Multiprocessing?**
   - **Answer**: Use **C-Extensions** (like NumPy or Cython) that explicitly release the GIL while performing their heavy C-based calculations.
10. **Q: What is the 'Join' method in threading?**
    - **Answer**: It tells the main program to "Wait here" until the specific thread has finished its execution.
11. **Q: What is the cost of creating a new Process vs. a new Thread?**
    - **Answer**: Processes are **Expensive** (they copy the whole RAM space). Threads are **Cheap** (they reuse the existing RAM space). 
12. **Q: What is 'Starvation' in concurrency?**
    - **Answer**: When a thread/process is perpetually denied the resources it needs to finish because other tasks are constantly being prioritized over it.
13. **Q: What is a 'Semaphore'?**
    - **Answer**: A lock that allows a **specific number** of threads to enter a block (e.g., "Allow only 5 threads to hit this external API at once").
14. **Q: Why is global state (global variables) dangerous in Threading?**
    - **Answer**: Because multiple threads can read and write to it simultaneously, leading to data corruption and non-deterministic logic.
15. **Q: What is the `multiprocessing.Pool` used for?**
    - **Answer**: To distribute a function call over a list of data across multiple CPU cores automatically.
16. **Q: Can you terminate a thread externally in Python?**
    - **Answer**: **No**. Python's threading library doesn't support hard termination because it could leave locks in an insecure state. You must use a "Flag" (like `is_running = False`) for the thread to check and exit gracefully.
17. **Q: What is a 'Thread-local Storage' (`threading.local`)?**
    - **Answer**: Data that is unique to each thread. Even if a global variable is shared, `threading.local` ensures each thread sees its own "private" version of that variable.
18. **Q: What is the 'Dining Philosophers' problem?**
    - **Answer**: A classic computer science example of **Resource Contention** and **Deadlocks**.
19. **Q: How does `multiprocessing` handle 'Zombie Processes'?**
    - **Answer**: By calling `join()` or having the parent process handle the exit signal. If a parent exits before a child, the child becomes an 'Orphan'.
20. **Q: What is the benefit of `concurrent.futures.as_completed()`?**
    - **Answer**: It yields results from a pool of tasks **as soon as they finish**, rather than waiting for them in the order they were started. This is much faster for heterogeneous network calls.

---

[← Previous: Generators](11-generators-iterators.md) | [Next: AsyncIO →](13-asyncio-concurrency.md)
