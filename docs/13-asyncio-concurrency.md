# 13. AsyncIO — High-Concurrency, Coroutines & Non-blocking I/O

> "AsyncIO is the 'Ferrari' of Python networking. It allows a single thread to handle thousands of simultaneous connections without the high overhead of multi-threading. An expert knows that one 'blocking' line of code can bring an entire async application to its knees."

---

## ❓ The 'Why' (High-Level)
In standard Python, when you call `requests.get()`, your whole script "stops and waits" for the server to reply. While it's waiting, the CPU is doing nothing. **AsyncIO** (Asynchronous I/O) allows your script to **Suspend** its work, let other code run while the network is busy, and resume as soon as the data arrives. This allows a single Python process to handle **100x more traffic** than traditional multi-threading.

---

## 🌱 Module 1: The Basics (Junior) — `async` & `await`
The core of async programming is the **Coroutine**.

### 1. `async def` and `await`
- **`async def`**: Defines a function as a "Coroutine" (it won't run immediately).
- **`await`**: Signals Python to "Pause" here if the work isn't done yet and let someone else use the CPU.
```python
import asyncio

async def say_hello():
    print("Hello...")
    await asyncio.sleep(1)  # Non-blocking wait!
    print("...World!")

asyncio.run(say_hello())
```

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — Running Tasks
To move beyond basics, you must run multiple things at once.

### 1. Concurrent Execution: `asyncio.gather()`
Instead of waiting for Task A, then B, then C, you can start all three at once.
```python
async def main():
    # Runs ALL three tasks simultaneously!
    await asyncio.gather(task1(), task2(), task3())
```

### 2. The Event Loop
AsyncIO runs on a single **Event Loop**. Think of it like a "Manager" that constantly checks: "Is the network data here? Yes? Okay, resume Task A."

---

## 🌳 Module 3: Advanced Mechanics (Senior) — Queues & Timeouts
Senior engineers protect their applications from "Hanging" forever.

### 1. Timeouts & Cancellation
Never wait for a network call without a timeout.
```python
try:
    result = await asyncio.wait_for(get_data(), timeout=5.0)
except asyncio.TimeoutError:
    print("The server was too slow!")
```

### 2. Mixing Sync and Async
What if you HAVE to use a library that doesn't support async (like `requests`)?
- **Expert fix**: Run the blocking code in a **Thread Pool** using `loop.run_in_executor()`.

---

## 🔥 Module 4: Principal Architect (Principal) — Loop Performance
At the highest level, you optimize the "Heart" of the system.

### 1. Blocking the Loop (The Cardinal Sin)
If you put `time.sleep(10)` or a `while True` loop inside an `async def`, the **Entire Event Loop stops**. Every other user on your web server will be stuck waiting for that one task to finish.
- **Principal check**: Use `asyncio` in **Debug Mode** to see "Slow Callback" warnings.

### 2. Custom Transports
For low-latency applications (like real-time trading), a principal engineer might bypass the high-level `asyncio` APIs and write a custom **Transport** or **Protocol** to handle raw TCP/UDP packets directly on the loop.

---

## 🏗️ Case Study: The 100,000 WebSocket Challenge
A messaging app needed to handle 100,000 users at once.
- **The Junior Approach**: Using `threading` (100k threads consume 20GB+ of RAM just for the "stacks"!).
- **The Principal Approach**: Used **AsyncIO** with the `uvloop` library (a faster C-based event loop).
- **Result**: Handled all 100k connections on a single server using only **2GB** of RAM and 15% CPU load.

---

## ⚡ Anti-Patterns & Expert Traps

### 1. Forgetting to `await`
If you call an async function without `await`, the code **will not run**. It will just return a "Coroutine Object" and move on.

### 2. Top-Level `asyncio.run()`
Avoid calling `asyncio.run()` multiple times in a single script. It's meant to be the **Single Entry Point** for your entire program.

---

## 🎯 Top 20 Principal Interview Questions (AsyncIO)

1. **Q: What is a 'Coroutine'?**
   - **Answer**: it is a special type of function that can "Suspend" its execution before it is finished, allowing other code to run on the same thread. It is defined using `async def`.
2. **Q: How does AsyncIO differ from Multi-threading?**
   - **Answer**: Multi-threading relies on the **OS** to switch between tasks (Preemptive). AsyncIO relies on the **Code** to give up control voluntarily (Cooperative). AsyncIO has much lower memory overhead.
3. **Q: What is the 'Event Loop'?**
   - **Answer**: The central orchestrator in AsyncIO that manages all running tasks, handles network I/O, and executes callbacks when results are ready.
4. **Q: What happens if you call `time.sleep()` inside an `async` function?**
   - **Answer**: It will **Block the entire Event Loop**, preventing all other scheduled tasks from running until the sleep is finished. Always use `await asyncio.sleep()`.
5. **Q: Explain `asyncio.gather()`.**
   - **Answer**: A utility to run multiple coroutines **Concurrently** and wait for all of them to finish, returning a list of their results.
6. **Q: What is a 'Future' in AsyncIO?**
   - **Answer**: An object that represents a **Result that hasn't happened yet**. It is a low-level bridge between a callback and a coroutine.
7. **Q: Explain `asyncio.create_task()`.**
   - **Answer**: It schedules a coroutine to run **In the background** immediately without waiting (awaiting) for it to finish first.
8. **Q: What is the purpose of `loop.run_in_executor()`?**
   - **Answer**: To run **Blocking** code (like heavy math or synchronous I/O) in a separate thread/process so it doesn't stop the main event loop.
9. **Q: What is 'uvloop'?**
   - **Answer**: A drop-in replacement for the standard AsyncIO event loop that is written in Cython. It is roughly 2-4x faster and used in high-performance web frameworks like FastAPI.
10. **Q: How do you cancel a running Task?**
    - **Answer**: By calling `task.cancel()`. This raises a `CancelledError` inside the coroutine, allowing it to perform cleanup (e.g., in a `finally` block).
11. **Q: What is an 'Async Iterator'?**
    - **Answer**: An object that implements `__aiter__` and `__anext__`, allowed to be used with `async for`. It's used for streaming data over a network.
12. **Q: What is an 'Async Context Manager'?**
    - **Answer**: An object that implements `__aenter__` and `__aexit__`, used with `async with`. It's standard for managing async resources like database connections.
13. **Q: Can one Event Loop run on multiple CPU cores?**
    - **Answer**: **No**. A single AsyncIO loop is strictly single-threaded. To use multiple cores, you must run one loop per CPU process.
14. **Q: What is 'Starvation' in an Event Loop?**
    - **Answer**: A situation where one long-running or CPU-intensive task refuses to `await`, preventing other tasks from ever getting a chance to run.
15. **Q: Explain `asyncio.wait_for`.**
    - **Answer**: It sets a maximum **Timeout** for a task. If the task doesn't finish in time, it is cancelled and a `TimeoutError` is raised.
16. **Q: What is the difference between `asyncio.run()` and `loop.run_until_complete()`?**
    - **Answer**: `asyncio.run()` is the modern (3.7+) way that creates a loop, runs the task, and closes the loop automatically. The other is a low-level manual approach.
17. **Q: How do you handle exceptions in `asyncio.gather()`?**
    - **Answer**: By default, an exception in one task will propagate. You can set `return_exceptions=True` to have the errors returned as values in the results list instead.
18. **Q: What is a 'Task'?**
    - **Answer**: A high-level object that wraps a Coroutine and manages its execution on the Event Loop.
19. **Q: Why is AsyncIO technically faster for thousands of I/O connections?**
    - **Answer**: Because it avoids the "Context Switching" overhead of the operating system having to swap out thousands of heavy thread stacks.
20. **Q: What is `asyncio.Queue` used for?**
    - **Answer**: To safely distribute work between async **Producers** and **Consumers** on the same event loop (e.g., a web scraper putting URLs into a queue for walkers).

---

[Previous: Concurrency](12-concurrency-threads-processes.md) | [Next: Testing & Mocking →](14-testing-mocking.md)
