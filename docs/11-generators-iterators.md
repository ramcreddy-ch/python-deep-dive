# 11. Generators & Iterators — Memory Efficiency & Streaming Pipelines

> "A list is for data that fits in RAM. A generator is for data that fits in your imagination. An expert uses Generators to process gigabytes of logs or trillions of rows without ever consuming more than a few megabytes of memory."

---

## ❓ The 'Why' (High-Level)
Modern applications often deal with "Infinite" or "Massive" data—social media feeds, server logs, or real-time stock prices. If you try to load 100GB of logs into a Python `list`, your application will crash instantly. **Generators** allow you to "Stream" data, processing one item at a time. This makes your software **Scalable** and **Memory-Efficient**.

---

## 🌱 Module 1: The Basics (Junior) — The `yield` Keyword
A normal function returns once and "dies." A generator "pauses" and remembers its state.

### 1. `return` vs `yield`
- **`return`**: Ends the function and gives back a final result.
- **`yield`**: Pauses the function, gives back a value, and waits for you to ask for the next one.
```python
def simple_gen():
    yield 1
    yield 2
    yield 3

g = simple_gen()
print(next(g)) # 1
print(next(g)) # 2
```

### 2. Iterator basics
An **Iterator** is an object you can call `next()` on. All generators are iterators.

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — Generator Expressions
Mid-level engineers use concise "One-liner" generators.

### 1. ( ) instead of [ ]
A **List Comprehension** `[x for x in data]` creates the entire list in memory immediately.
A **Generator Expression** `(x for x in data)` creates an object that calculates values **only when you ask for them**.
```python
# Creates a 1,000,000 item list (Heavy)
list_sq = [x*x for x in range(1000000)]

# Creates a generator object (Light)
gen_sq = (x*x for x in range(1000000))
```

### 2. The `next()` function
Generators are "Lazy." They don't do any work until you call `next()`. Once the generator is empty, it raises a **StopIteration** exception.

---

## 🌳 Module 3: Advanced Mechanics (Senior) — Two-Way Pipelines
Senior engineers use generators to not just *get* data, but to *send* it.

### 1. Using `.send()`
You can push data back into a generator while it is paused. This turns a generator into a **Coroutine**.
```python
def printer():
    while True:
        value = yield  # Pause and wait for a value
        print(f"Received: {value}")

p = printer()
next(p)      # 'Prime' the generator (start it)
p.send(10)   # Outputs: Received: 10
```

### 2. `yield from` (Delegation)
If you have multiple generators, you can chain them using `yield from`. This is much cleaner than a manual loop.

---

## 🔥 Module 4: Principal Architect (Principal) — Generator Lifecycle
At the highest level, you manage the internal states of the generator.

### 1. Generator States
A generator can be in one of four states:
1.  **GEN_CREATED**: Waiting to start.
2.  **GEN_RUNNING**: Currently executing code.
3.  **GEN_SUSPENDED**: Paused at a `yield`.
4.  **GEN_CLOSED**: Finished or terminated.

### 2. Memory Footprint calculation
A generator object itself takes about **80 bytes** of memory regardless of whether it represents 10 integers or 10 billion integers. This is the "Magic" of streaming.

---

## 🏗️ Case Study: The 1TB Log Processor
A cloud security company had to process 1 terabyte of log data daily on a small 4GB RAM server.
- **The Junior Approach**: Trying to read the whole file or chunks into a list. (Exhausted RAM in seconds).
- **The Principal Approach**: Built a **Pipeline of Generators**.
  - `gen1`: Reads the file line-by-line (Lazy).
  - `gen2`: Filters for errors (Lazy).
  - `gen3`: Extracts IP addresses (Lazy).
- **Result**: The entire 1TB file was processed in a single pass using only **32MB** of RAM.

---

## ⚡ Anti-Patterns & Expert Traps

### 1. Casting to a List
**NEVER** do `list(my_generator)` if the generator represents a massive dataset. This defeats the entire purpose of a generator and will crash your application.

### 2. Reusing a Generator
Once a generator is finished, it is empty. You cannot "reset" it. If you need to iterate again, you must create a **New** generator instance.

---

## 🎯 Top 20 Principal Interview Questions (Generators & Iterators)

1. **Q: What is a Generator in Python?**
   - **Answer**: It is a special type of iterator—a function that uses the `yield` keyword to return values one at a time, pausing its execution state between each one.
2. **Q: How does `yield` differ from `return`?**
   - **Answer**: `return` terminates the function and sends back a value. `yield` pauses the function, sends a value, and allows the function to resume from that exact spot later.
3. **Q: What is an 'Iterator'?**
   - **Answer**: An object that implements the `__next__` and `__iter__` methods. It is an object you can call `next()` on to get the next series of data.
4. **Q: Explain 'Lazy Evaluation' in the context of generators.**
   - **Answer**: Values are calculated only and exactly when they are requested. This allows you to work with datasets that are larger than your available memory.
5. **Q: What is a 'Generator Expression'?**
   - **Answer**: A high-performance, single-line way to create a generator object. It looks like a list comprehension but uses parentheses `()` instead of square brackets `[]`.
6. **Q: What is the `StopIteration` exception?**
   - **Answer**: It is the signal raised by an iterator's `__next__` method to tell a `for` loop (or the caller) that there are no more items to be produced.
7. **Q: What is the purpose of the `.send()` method?**
   - **Answer**: It allows you to **Inject a value** back into the generator where it was paused at a `yield` statement, allowing for two-way communication.
8. **Q: What does `yield from` do?**
   - **Answer**: It delegates the generator's operations to a sub-generator. It's a cleaner way to "chain" multiple generators together.
9. **Q: How do you "prime" a generator?**
   - **Answer**: By calling `next(gen)` or `gen.send(None)` to start its execution before you can send it any real data.
10. **Q: What is the memory complexity of a generator?**
    - **Answer**: **O(1)**. The memory usage remains constant regardless of how many items the generator will eventually produce.
11. **Q: What happens if a generator raises an unhandled exception?**
    - **Answer**: The exception propagates to the code that called `next()`, and the generator becomes **Closed** (it cannot be resumed).
12. **Q: Can a generator have a `return` statement?**
    - **Answer**: Yes. In Python 3, a `return` inside a generator raises `StopIteration` and sets the return value as the exception's value.
13. **Q: Explain the `itertools` module.**
    - **Answer**: A library of "Iterator Building Blocks" for high-performance, memory-efficient data processing (e.g., `chain`, `cycle`, `islice`).
14. **Q: What is the difference between an 'Iterable' and an 'Iterator'?**
    - **Answer**: An **Iterable** is an object you can get an iterator from (e.g., a list or string). An **Iterator** is the object that actually performs the iteration (calls `next()`).
15. **Q: Why can't you "reset" a generator?**
    - **Answer**: Because a generator is a **one-way stream**. Once the internal function reaches the end or a return statement, its stack frame is destroyed.
16. **Q: What is the `close()` method in a generator?**
    - **Answer**: A method that manually terminates the generator by raising a `GeneratorExit` exception inside it.
17. **Q: How do you handle 'Resource Cleanup' in a generator?**
    - **Answer**: By using a `try...finally` block inside the generator. The `finally` block will run even if the generator is closed early via `.close()`.
18. **Q: What is 'Infinite Sequence' generation?**
    - **Answer**: Using a `while True` loop inside a generator to produce values forever (e.g., a counter or heartbeat). They are safe to use as long as they are only consumed one-by-one.
19. **Q: What is the `inspect.getgeneratorstate()` function used for?**
    - **Answer**: To check the current lifecycle status of a generator (Created, Running, Suspended, or Closed).
20. **Q: What is a 'Coroutine' in the context of generators?**
    - **Answer**: A generator that is used as a consumer of data (using `.send()`) rather than just a producer. This was the basis for asynchronous programming in Python before the `async/await` syntax.

---

[Previous: Decorators](10-decorators-context-managers.md) | [Next: Concurrency →](12-concurrency-threads-processes.md)
