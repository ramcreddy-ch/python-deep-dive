# 24. Performance & Profiling — Bottlenecks, GIL & Data Ops

> "Premature optimization is the root of all evil. But delayed optimization is why your AWS bill is $50,000 this month. An expert doesn't 'guess' why a script is slow; they use profilers to find the exact line of code that is killing the CPU."

---

## 🌱 The Basics: Time & Memory
The entry-level way to check performance is to measure **Wall Clock Time** (how long it takes to run).

```python
import time

start = time.time()
# Your slow code here...
# data = [i**2 for i in range(1000000)]
end = time.time()

print(f"Time Taken: {end - start:.4f} seconds")
```

---

## 🌿 Intermediate: Profiling (cProfile)
`cProfile` is a built-in "Stopwatch" that tracks every single function call and how long it took.

**Real Use (DevOps/SRE)**:
Finding why a 1,000-line automation script is taking 5 minutes to run.

```python
import cProfile

def my_slow_app():
    # ... logic here ...
    pass

# Run to see a detailed report of every function
# cProfile.run('my_slow_app()')
```

---

## 🌳 Advanced: Memory Optimization
Senior engineers use **Generators** and **__slots__** to minimize the "Memory Footprint" of an application.

**The Benchmark**: 
Creating 1 million objects with and without `__slots__`.

```python
import sys

class BasicUser:
    def __init__(self, id):
        self.id = id

class OptimizedUser:
    """
    Expert Pattern: Memory Hardening. 
    Demonstrates: Removing __dict__ overhead.
    """
    __slots__ = ['id']
    def __init__(self, id):
        self.id = id

# sys.getsizeof(BasicUser(1)) # Memory-heavy (has a __dict__)
# sys.getsizeof(OptimizedUser(1)) # Memory-light (fixed array)
```

---

## 🔥 Expert: The GIL & Parallelism
Principal engineers use **Cython** or **Rust** for the "Critical Path" (the 5% of code that handles 95% of the data).

### 1. Bypassing the GIL
By moving performance-heavy math to a C-extension, you can release the GIL and achieve true multi-core parallelism.

### 2. Pypy & JIT
Sometimes, the best performance boost comes from switching the **Runtime**. Pypy is a Just-In-Time (JIT) compiler that can be 5x-10x faster than standard Python for long-running math tasks.

---

## 🎯 Top 20 Principal Interview Questions (Performance & Profiling)

1. **Q: What is 'Time Complexity' (Big O)?**
   - **Answer**: It is a way to describe how much slower an algorithm gets as the data grows. `O(1)` is instant (Dictionary lookup). `O(n)` is linear (Scanning a list). `O(n^2)` is squared (Nested loops). An expert always aims for the lowest Big O possible.
2. **Q: When should you use a 'Sampling' Profiler (like Py-Spy)?**
   - **Answer**: `cProfile` adds a lot of overhead. If you want to profile a live **Production Server** without slowing it down for users, you use a "Sampling" profiler that just "Peeks" (samples) at the stack every few milliseconds.
3. **Q: What is the 'GIL' and how does it impact Multi-Threading?**
   - **Answer**: The Global Interpreter Lock allows only one thread to execute Python bytecode at a time. This means multi-threading in Python doesn't provide a speed boost for **CPU-Bound** tasks, even on a 64-core machine.
4. **Q: How does `__slots__` save memory?**
   - **Answer**: By preventing the creation of a `__dict__` for every instance. It uses a fixed-size array instead of a hash table, saving significant RAM when creating millions of small objects.
5. **Q: What is the difference between `list.append()` and `list.insert(0, x)`?**
   - **Answer**: `append()` is **O(1)** (constant time). `insert(0, x)` is **O(n)** (linear time) because Python must "Shift" every other item in the list to make room at the front.
6. **Q: Explain 'Memoization'.**
   - **Answer**: It's a strategy where you store the results of expensive function calls (using a dictionary) and return the cached result if the same inputs occur again. Use `functools.lru_cache`.
7. **Q: What are 'Cache Locality' and 'Data Contiguity'?**
   - **Answer**: The concept that data stored close together in RAM is faster to access. Python lists are arrays of pointers (non-contiguous), while **NumPy arrays** are contiguous blocks of raw data, making NumPy much faster for mathematical operations.
8. **Q: When is `PyPy` a better choice than `CPython`?**
   - **Answer**: When you have a long-running, CPU-bound application written in pure Python. PyPy's JIT compiler can provide a 5x-10x speed boost.
9. **Q: What is a 'Memory Leak' in Python?**
   - **Answer**: When objects are no longer needed but are still referenced (e.g., in a global list or a circular reference), preventing the Garbage Collector from freeing the RAM.
10. **Q: How do you profile 'Memory Usage' specifically?**
    - **Answer**: Use the **`memory_profiler`** library with the `@profile` decorator to see a line-by-line breakdown of RAM consumption.
11. **Q: What is the benefit of `array.array` over a standard `list`?**
    - **Answer**: It is more memory-efficient because it only stores raw machine values (like a C-array) instead of full Python objects.
12. **Q: How does 'Garbage Collection' impact performance?**
    - **Answer**: The GC pauses your application to scan for objects to delete. This can cause "Stutters" in high-speed applications. Experts minimize this by reusing objects instead of constantly creating new ones.
13. **Q: What is 'Premature Optimization'?**
    - **Answer**: Trying to make code faster before you know where the actual bottleneck is. Use a profiler **first** before changing any complex code.
14. **Q: What is 'Vectorization' in the context of performance?**
    - **Answer**: The practice of performing operations on entire arrays at once (using SIMD) instead of looping through items manually.
15. **Q: How do you optimize 'String Concatenation' in a long loop?**
    - **Answer**: Use **`.join()`**. Using `+` in a loop creates a new string object every time, which is extremely slow (O(n^2)).
16. **Q: What is a 'Hot Path' in code?**
    - **Answer**: The specific lines of code that are executed most frequently and consume the most CPU time. This is where 99% of optimization effort should be spent.
17. **Q: What is the purpose of `sys.setrecursionlimit()`?**
    - **Answer**: To increase the maximum depth of the call stack for recursive functions. Warning: Setting it too high can cause a real OS segmentation fault.
18. **Q: How do you handle 'I/O Bound' performance issues?**
    - **Answer**: Using **Multi-threading**, **AsyncIO**, or **Buffering**. Performance is lost waiting for the disk/network, so you want to switch tasks while waiting.
19. **Q: What is 'Just-In-Time' (JIT) compilation?**
    - **Answer**: The process of compiling bytecode into machine code **during execution** based on which parts of the code are run most often.
20. **Q: What is the `dis` module used for?**
    - **Answer**: To disassemble Python source code into its underlying **Bytecode**. This allows a principal engineer to see exactly how the interpreter is executing their logic.

---

[← Previous: LLMOps](../Level-3/23-llm-engineering.md) | [Next: Advanced Security →](25-advanced-security.md)
