# 13. AsyncIO: High-Concurrency APIs — non-blocking I/O & Event Loops

> "AsyncIO is the 'Secret Sauce' of modern high-performance Python. It allows you to handle thousands of concurrent network connections on a single CPU thread, making it the choice for building production APIs, chat services, and realtime data scrapers."

---

## 🌱 The Basics: `async` & `await`
AsyncIO doesn't use threads; it uses **Coroutines**. A coroutine "Pauses" itself when waiting for I/O, allowing other coroutines to run on the same thread.

```python
import asyncio

async def say_hello():
    print("Hello...")
    await asyncio.sleep(1) # 'Pauses' here, doesn't block the CPU!
    print("...World!")

# To run it, you need an Event Loop
# asyncio.run(say_hello())
```

---

## 🌿 Intermediate: Running Multiple Tasks
Senior engineers use **`asyncio.gather()`** to run many network tasks at once.

**Real Use (API Client)**:
Fetching data from 5 different services simultaneously.

```python
async def fetch_srv(name):
    # Simulate API call
    await asyncio.sleep(1)
    return f"{name} Data"

async def main():
    # Start all 3 at once!
    results = await asyncio.gather(
        fetch_srv("A"),
        fetch_srv("B"),
        fetch_srv("C")
    )
    print(results)

# asyncio.run(main())
```

---

## 🌳 Advanced: The Event Loop & Non-Blocking I/O
The **Event Loop** is the "Heart" of AsyncIO. It is a single-threaded loop that checks which tasks are "Ready" (e.g., a network packet arrived) and runs them one by one.

**Expert Warning**:
If you call a "Blocking" function (like `time.sleep()` or `requests.get()`) inside an `async` function, the **Entire Event Loop stops**. No other task can run. You Must use async-compatible libraries like `aiohttp` or `httpx`.

---

## 🔥 Expert: Async Context Managers & Iterators
Principal engineers use `async with` and `async for` to manage resources that require network calls during setup/teardown.

```python
class AsyncDatabase:
    """
    Expert Pattern: Async Lifecycle. 
    Demonstrates: Non-blocking resource management.
    """
    async def __aenter__(self):
        # Open DB connection (non-blocking)
        # await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        # Close DB connection (non-blocking)
        # await self.disconnect()
        pass

# Usage
# async with AsyncDatabase() as db:
#     await db.query("SELECT * FROM users")
```

---

## 🎯 Top 20 Principal Interview Questions (AsyncIO)

1. **Q: What is the primary difference between `await` and `return`?**
   - **Answer**: `return` finishes the function and sends back a value. `await` **Suspends** the function temporarily, giving control back to the Event Loop, and resumes only when the awaited task is complete.
2. **Q: What is a 'Coroutine'?**
   - **Answer**: It is a specialized function (defined with `async def`) that can be paused and resumed. Unlike normal functions, they don't run immediately; they return a **Coroutine Object** that must be scheduled in an Event Loop.
3. **Q: What is the 'Event Loop'?**
   - **Answer**: The central manager that keeps track of all running coroutines. it continuously loops and executes tasks that are "Ready" for work.
4. **Q: Why should you never use `time.sleep()` in an async function?**
   - **Answer**: Because `time.sleep()` is **Blocking**. It prevents the entire Event Loop from running, which stops all other concurrent tasks. Use `await asyncio.sleep()` instead.
5. **Q: What is the difference between `asyncio.gather()` and `asyncio.wait()`?**
   - **Answer**: `gather()` is higher-level; it waits for all tasks to finish and returns their results in order. `wait()` gives you more control, returning two sets: "Done" and "Pending" tasks as they complete.
6. **Q: What is `asyncio.create_task()` used for?**
   - **Answer**: It "Backgrounds" a coroutine. It starts the task and continues executing the current code immediately without waiting for the task to finish.
7. **Q: What is an 'Async Context Manager'?**
   - **Answer**: An object that implements `__aenter__` and `__aexit__`. It allows you to use `async with` to manage resources that require non-blocking I/O for connection/cleanup.
8. **Q: How can you run a 'Blocking' function (like a heavy math task or a legacy library) inside an async function without freezing the loop?**
   - **Answer**: Use `loop.run_in_executor()`. This sends the blocking function to a separate thread while the main Event Loop stays responsive.
9. **Q: What is `awaitable` in Python?**
   - **Answer**: Any object that can be used with the `await` keyword. Examples include Coroutines, Tasks, and Futures.
10. **Q: Can you define an `async __init__` method in a class?**
    - **Answer**: **No**. `__init__` must be a synchronous method. To perform async setup for a class, use a "Factory Method" (e.g., `await MyClass.create()`).
11. **Q: What is an 'Aiohttp' and why is it preferred over 'Requests'?**
    - **Answer**: `Requests` is a blocking library. `Aiohttp` is an asynchronous HTTP client/server that allows you to make 1,000 requests concurrently without waiting for each one to finish before starting the next.
12. **Q: Explain the `StopAsyncIteration` exception.**
    - **Answer**: It is the async version of `StopIteration`, used by `async for` loops to know when an asynchronous generator has finished its data stream.
13. **Q: What is a 'Future' in AsyncIO?**
    - **Answer**: A low-level object that represents a result that **hasn't arrived yet**. It's a "Promise" that something will happen in the future.
14. **Q: What is the `asyncio.run()` function introduced in 3.7?**
    - **Answer**: The standard entry point for an async application. It creates the event loop, runs the main coroutine, and shuts down the loop properly when finished.
15. **Q: How do you handle 'Timeouts' in AsyncIO?**
    - **Answer**: Use `asyncio.wait_for(coro, timeout=5)`. It will raise a `TimeoutError` if the task takes longer than the specified time.
16. **Q: What is an 'Async Iterable'?**
    - **Answer**: An object that can be used with `async for`. It implements `__aiter__` and its `__anext__` method must be a coroutine.
17. **Q: Why is AsyncIO often called "Cooperative Multitasking"?**
   - **Answer**: Because tasks must **Cooperate** by yielding control (via `await`) to allow others to run. In "Pre-emptive" threading, the OS forces tasks to stop.
18. **Q: How many event loops can run in a single thread?**
    - **Answer**: Only **one** active event loop can run per thread at any given time.
19. **Q: What is the purpose of `asyncio.shield()`?**
    - **Answer**: To protect a task from being cancelled even if the encompassing operation is cancelled.
20. **Q: What is a 'Task' in AsyncIO?**
    - **Answer**: A subclass of Future that wraps a coroutine and manages its execution state within the event loop.

---

[← Previous: Concurrency](12-concurrency-threads-processes.md) | [Next: Testing →](14-testing-mocking.md)
