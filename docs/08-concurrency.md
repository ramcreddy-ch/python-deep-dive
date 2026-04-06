# 08. Concurrency & Parallelism — Production Deep Dive

> The single biggest hurdle transitioning from junior to senior engineering is mastering execution models. Python's Global Interpreter Lock (GIL) is infamous, but platform engineers must know exactly when to bypass it with Processes, circumvent it with AsyncIO, or yield to it with Threads.

---

## 🔍 The Concurrency Models in Python

| Model | Module | Best For | GIL Impact | Core Mechanic |
|-------|--------|----------|------------|---------------|
| **Threading** | `threading` | I/O-bound (File/Network/DB) | Blocks execution | Shared memory space |
| **Multiprocessing** | `multiprocessing` | CPU-bound (Data/Maths/Images) | Bypasses GIL entirely | Separate memory, IPC needed |
| **AsyncIO** | `asyncio` | High-throughput network I/O | Blocks on CPU tasks | Single-thread event loop |

### The Global Interpreter Lock (GIL)
The GIL is a mutex that protects access to Python objects, preventing multiple native threads from executing Python bytecodes at once. 
*   **Result**: Multi-threading in Python *does not* utilize multiple CPU cores for raw calculation.
*   **Caveat**: I/O operations (HTTP requests, sleep, DB queries, C-extensions like NumPy) voluntarily *release* the GIL. Threads are amazing for networking!

---

## 🏭 Threading: Best for API Calls (Platform Engineering)

A platform script querying 1,000 Kubernetes pods sequentially takes 1,000 seconds. A ThreadPool executor drops this to 20 seconds.

```python
import concurrent.futures
import requests

URLS = ["http://api.service.com/health"] * 100

def check_health(url):
    # This blocks HTTP, not the CPU. The GIL is released during the network wait.
    res = requests.get(url, timeout=5)
    return res.status_code

# ThreadPoolExecutor creates a pool of OS-level threads.
# Max_workers ensures we don't open 100 simultaneous sockets and crush the API.
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    # Map automatically distributes the URL pool across the worker threads
    results = list(executor.map(check_health, URLS))

print(f"Completed {len(results)} health checks.")
```

---

## ⚙️ Multiprocessing: Best for Feature Engineering (MLOps)

When transforming images, doing heavy math, or crunching parquet files, Threading fails. We must spawn explicit separate processes, each containing its own isolated Python interpreter and GIL.

```python
import concurrent.futures
import math

# A heavy CPU operation
def crunch_numbers(number):
    return math.factorial(number)

numbers = [10000, 15000, 20000, 25000]

if __name__ == '__main__':
    # ProcessPoolExecutor forks our script across multiple actual CPU cores
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(crunch_numbers, numbers))
    print("Crunching complete!")
```

> **Warning:** Processes don't share memory. Passing objects between them relies on Serialization (Pickle), which is a massive bottleneck. If you pass a 10GB object to a process, Python literally copies 10GB of RAM.

---

## 🚀 AsyncIO: The Modern Asynchronous standard (Cloud/SRE)

Standard threads consume ~4MB of RAM per thread. You cannot scale out to 10,000 connections using Threads (you would OOM the OS). `asyncio` uses a single thread with an Event Loop, juggling lightweight coroutines. This is how FastAPI achieves Node.js/Go-level routing speeds.

```python
import asyncio
import aiohttp

async def fetch_data(session, url, idx):
    """Coroutines map cleanly to API behaviors."""
    print(f"Starting req {idx}")
    # The 'await' keyword pauses this function, returning control to the 
    # Event Loop to do other work until the network responds.
    async with session.get(url) as response:
        data = await response.text()
        print(f"Finished req {idx}")
        return len(data)

async def main():
    urls = ["http://python.org"] * 5
    # The aiohttp session manages connection pooling
    async with aiohttp.ClientSession() as session:
        # Schedule all tasks to run concurrently
        tasks = [fetch_data(session, url, i) for i, url in enumerate(urls)]
        # Gather waits until all tasks are complete
        results = await asyncio.gather(*tasks)
        print("All done:", results)

# To kickstart the whole event loop:
# asyncio.run(main())
```

---

## 🤖 AI / GPU Perspective

### Distributed Data Parallel (PyTorch)
In deep learning, we bypass Python's limitations natively by handing off control. PyTorch's `DistributedDataParallel` (DDP) spawns distinct Python processes (one for each GPU block) using OS-level multi-processing. The C++ backend (NCCL) then does all the heavy cross-GPU communication natively, bypassing Python IPC and the GIL entirely.

---

## 🎯 Senior Engineer Interview Questions

**Q1: If `asyncio` runs on a single thread and a single core, how is it concurrent?**
> **Answer:** Concurrency does not mean running at the exact same physical millisecond (that is *parallelism*). Concurrency is about executing out of order. When Python hits an `await` statement on a network call, the OS intercepts that network blocking operation. The Python event loop instantly switches to executing another coroutine. Through asynchronous context switching, one thread can manage thousands of open sockets simultaneously without ever idling waiting for a byte of data to return.

**Q2: We put a heavy Pandas data transformation inside a FastAPI `async def` endpoint. What happens to the REST API?**
> **Answer:** The entire API hard-freezes for all users. `async def` functions run within the single thread of the asyncio event loop. Pandas computations are CPU-bound and do not yield `await` control to the loop. While Pandas crunches data, the event loop is blocked, meaning no new incoming HTTP requests can be accepted or responded to. Heavy computations in async APIs must be offloaded using `run_in_executor()` to push them onto a separate thread or process pool.

**Q3: Explain the difference between `multiprocessing.Queue` and a standard Python `.queue`.**
> **Answer:** The standard `queue.Queue` is designed to be thread-safe for threads operating within a single shared memory space. A `multiprocessing.Queue` operates across distinct processes. Under the hood, it utilizes an OS pipe and a background thread to serialize (Pickle), transmit, and deserialize objects across isolated memory spaces.

**Q4: Will the GIL ever be removed from Python?**
> **Answer:** Yes, it is actively happening right now. PEP 703 (Making the Global Interpreter Lock Optional in CPython) was accepted. Starting in heavily experimental phases around Python 3.13+, CPython will offer a build that disables the GIL. However, shifting the ecosystem (especially C-extensions) to support Free-Threading is expected to take 5+ years of transition.

---

[← Previous: Decorators & Generators](07-decorators-generators.md) | [Back to Index](../README.md) | [Next: Python for DevOps →](09-python-devops.md)
