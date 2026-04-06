# 11. Generators & Iterators — Memory Efficiency & Streaming Pipelines

> "A list is for data that fits in RAM. A generator is for data that fits in your imagination. An expert uses Generators to process gigabytes of logs or trillions of rows without crashing the application with 'MemoryError'."

---

## 🌱 The Basics: Iterators & Loops
An **Iterator** is an object that yields its next item when you call `next(it)`. 

- **Iterable**: Any object (list, tuple, string) that can provide an iterator.
- **Iteration**: The process of going through items one by one.

```python
# A list is an iterable
names = ["Alice", "Bob"]
it = iter(names) # Get the iterator

# Manual iteration
print(next(it)) # Alice
print(next(it)) # Bob
# print(next(it)) # Throws StopIteration!
```

---

## 🌿 Intermediate: Generator Functions (`yield`)
A generator is a function that uses **`yield`** instead of `return`. 

**Why?** Unlike `return`, which gives back all values at once, `yield` pauses the function and gives back one value at a time.

```python
def count_to_three():
    yield 1
    yield 2
    yield 3

# Usage
for num in count_to_three():
    print(num)
```

---

## 🌳 Advanced: Memory Impact (List vs. Generator)
At the senior level, we use generators to optimize performance. 

**The Benchmark**: 
Creating a list of 1 million integers vs. a generator of 1 million integers.

```python
import sys

# 1. Memory-Heavy (List)
# Every number is stored in RAM instantly.
large_list = [i for i in range(1000000)]
print(f"List Size: {sys.getsizeof(large_list) / 1024 / 1024:.2f} MB")

# 2. Memory-Efficient (Generator Expression)
# No numbers are stored; it only knows how to 'generate' them.
large_gen = (i for i in range(1000000))
print(f"Generator Size: {sys.getsizeof(large_gen):.2f} BYTES")
```

---

## 🔥 Expert: Streaming Data Pipelines
Principal engineers use generators to build "Pipelines" that process data as it flows, without storing it.

**Real Use (SRE/Log Analysis)**:
Scanning a 10GB log file for errors.

```python
def log_lines(filename):
    """
    Expert Pattern: Data Streaming. 
    Demonstrates: Memory-safe log parsing.
    """
    with open(filename, "r") as f:
        for line in f:
            yield line # Yield one line at a time

def filter_errors(lines):
    for line in lines:
        if "ERROR" in line:
            yield line # Further filtering in a pipeline

# Usage
# pipeline = filter_errors(log_lines("prod_access.log"))
# for error in pipeline:
#     print(error) # Only the high-impact lines are ever in RAM!
```

---

## 🎯 Top 20 Principal Interview Questions (Generators & Iterators)

1. **Q: What is a Generator in Python?**
   - **Answer**: It is a special type of iterator that yields values one-at-a-time using the `yield` keyword. It saves memory because it doesn't store the entire collection in RAM.
2. **Q: What is the difference between `yield` and `return`?**
   - **Answer**: `return` terminates a function and returns a value. `yield` pauses the function, returns a value, and allows it to resume from that exact spot later.
3. **Q: Explain the `StopIteration` exception.**
   - **Answer**: It is a signal raised by an iterator when it has no more items to yield. Python's `for` loop catches this automatically and exits the loop gracefully.
4. **Q: What is an 'Iterable' vs an 'Iterator'?**
   - **Answer**: An **Iterable** is an object you can iterate over (like a List or String). An **Iterator** is the object that actually tracks the "position" in the collection and yields the next item via `next()`.
5. **Q: How can you check if an object is an Iterator?**
   - **Answer**: Use `isinstance(obj, collections.abc.Iterator)`.
6. **Q: What is a 'Generator Expression'?**
   - **Answer**: A concise way to create a generator in one line: `(i**2 for i in range(10))`. It is the same syntax as a list comprehension but uses `()` instead of `[]`.
7. **Q: Can you restart a generator once it is finished?**
   - **Answer**: **No**. Generators are one-way streams. Once you exhaust them, they are gone. You must create a new generator instance to iterate again.
8. **Q: What is the purpose of `yield from`?**
   - **Answer**: It allows a generator to delegate part of its operations to another generator. It's a cleaner way to write "Nested" generators.
9. **Q: How much memory does a generator of 1 billion items take?**
   - **Answer**: Very little (usually ~100-200 bytes). It only stores the current state and the logic for the next item, not the 1 billion items themselves.
10. **Q: Explain the `send()` method in a generator.**
    - **Answer**: It allows you to **Inject** a value back into the generator where it last yielded. This turns a generator into a **Co-routine**. 
11. **Q: What is the `close()` method used for?**
    - **Answer**: To tell a generator to stop yielding and exit immediately, raising a `GeneratorExit` exception inside it. 
12. **Q: Can a generator have a `return` statement?**
    - **Answer**: Yes. In Python 3+, a `return` in a generator raises `StopIteration` and stores the returned value in the exception object.
13. **Q: What is 'Lazy Evaluation'?**
    - **Answer**: The strategy of delaying a calculation until it is absolutely required. Generators are the primary tool for lazy evaluation in Python.
14. **Q: How do you build an 'Infinite' generator?**
    - **Answer**: Use a `while True` loop inside a generator function: `while True: yield i; i += 1`.
15. **Q: What is `itertools.islice()`?**
    - **Answer**: It allows you to "Slice" a generator (e.g., get only items 10 to 20) without loading the whole thing into a list first.
16. **Q: Why use generators for Log Processing?**
    - **Answer**: Because production logs can be gigabytes or terabytes in size. Generators allow you to process the log line-by-line using only a few kilobytes of RAM.
17. **Q: What is the difference between `iter()` and `__iter__`?**
    - **Answer**: `iter(obj)` is the built-in function that calls the `obj.__iter__()` dunder method of the object.
18. **Q: Can you use indexing (e.g., `gen[0]`) on a generator?**
    - **Answer**: **No**. Generators do not support indexing because they don't store the items in memory.
19. **Q: What is a 'Pipeline' in generative programming?**
    - **Answer**: Connecting multiple generators together (`gen3(gen2(gen1(data)))`) so that data flows through multiple transformations one-by-one without any intermediate lists.
20. **Q: What is the `sys.getsizeof()` of a generator object?**
    - **Answer**: It is constant, regardless of how many items the generator will produce, because it only stores the bytecode state and local variables.

---

[← Previous: Decorators](10-decorators-context-managers.md) | [Next: Concurrency →](12-concurrency-threads-processes.md)
