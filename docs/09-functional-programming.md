# 09. Functional Programming — Lambda, Map, Filter & Immutability

> "Functional programming isn't about functions; it's about avoiding 'Side Effects' and treating data as a 'Transformation'. An expert uses functional patterns to build clean, predictable, and highly testable data processing pipelines."

---

## 🌱 The Basics: Lambda Functions
A **Lambda** is an "Anonymous Function" — a one-liner that doesn't need a `def` name.

```python
# Standard function
def add_ten(x):
    return x + 10

# Lambda version
add_ten_lambda = lambda x: x + 10

# Usage
print(add_ten_lambda(5)) # 15
```

---

## 🌿 Intermediate: Map, Filter & Zip
These are the core "Workhorse" functions for processing collections. 

- **Map**: Apply a function to **every** item in a list.
- **Filter**: Keep only the items that pass a **truth test**.

```python
nums = [1, 2, 3, 4, 5, 6]

# 1. Map: Double all numbers
doubled = list(map(lambda x: x * 2, nums))

# 2. Filter: Keep only evens
evens = list(filter(lambda x: x % 2 == 0, nums))
```

---

## 🌳 Advanced: High-Level Transformations (Functools)
Python's `functools` library provides "Experts-Only" tools for complex function manipulation.

### 1. `partial`
Pre-filling some arguments of a function to create a new, simpler one.

```python
from functools import partial

# A generic function
def send_alert(message, level="INFO"):
    print(f"[{level}] {message}")

# 2. Create a specialized version
critical_alert = partial(send_alert, level="CRITICAL")

# Usage
critical_alert("Database Offline!") # level="CRITICAL" is automatic!
```

---

## 🔥 Expert: Immutability & Side Effects
At the principal level, you must understand **Why** you use functional patterns.

### 1. Avoiding Side Effects
A function should not change anything *outside* itself (like a global variable or a mutable list). This makes code "Concurrent-Safe."

### 2. The Multi-Core Goal
Functional code (using Map/Filter) is easier to parallelize across 64 CPU cores because the data flows in ONE direction and never changes in-place.

```python
# Expert Pattern: Pure Functions. 
# Demonstrates: Returning NEW data instead of modifying 'old' data.
def process_user_data(user_dict):
    """
    Principal Pattern: Functional Pure Function.
    The original user_dict is NEVER touched.
    """
    # Create a fresh copy with the transformation
    return {**user_dict, "last_login": "2024-04-06"}
```

---

## 🎯 Top 20 Principal Interview Questions (Functional Programming)

1. **Q: What is a 'Pure Function'?**
   - **Answer**: A function that has no **Side Effects** and always returns the same output for the same input. It doesn't modify global variables or input objects.
2. **Q: What are the benefits of 'Immutability'?**
   - **Answer**: Code is easier to reason about, safer for **Concurrency/Parallelism**, and less prone to accidental data corruption bugs.
3. **Q: What is a 'Lambda' function?**
   - **Answer**: An anonymous, one-line function that can be defined without a name. It is "Syntactic Sugar" for a full function definition.
4. **Q: Explain the difference between `map()` and a 'List Comprehension'.**
   - **Answer**: Functionally, they are very similar. `map()` returns a **Lazy Iterator** (saving memory). List comprehension returns a **List** (consuming memory). List comprehension is generally considered more Pythonic.
5. **Q: What is `functools.reduce()`?**
   - **Answer**: A function that reduces an entire list to a **single value** by applying a binary operation (e.g., summing all numbers or finding the maximum).
6. **Q: What is a 'Higher-Order Function'?**
   - **Answer**: A function that either takes another function as an argument (like `filter`) or returns a function (like a decorator).
7. **Q: Explain `functools.partial`.**
   - **Answer**: It allows you to "Pre-fill" some arguments of a function to create a new, simplified function. 
8. **Q: What is 'Currying' in functional programming?**
   - **Answer**: The technique of transforming a function that takes multiple arguments into a sequence of functions that each take a single argument.
9. **Q: Why are 'Recursion' and 'Immutability' often linked?**
   - **Answer**: In pure functional languages, you don't use loops (which require a mutable 'counter' variable). You use recursion instead to process data.
10. **Q: What is `functools.lru_cache`?**
    - **Answer**: A decorator that adds **Memoization** (caching) to a function. It stores previous results and returns them instantly if the same inputs occur again.
11. **Q: What is a 'Closure'?**
    - **Answer**: A nested function that remembers the environment in its enclosing scope. This allows it to access variables from the outer function even after that function has finished.
12. **Q: What is a 'Predicate' in functional programming?**
    - **Answer**: A function that returns a boolean (`True` or `False`). It is used inside `filter()` to decide which items to keep.
13. **Q: Does Python support 'Tail Call Optimization' (TCO)?**
    - **Answer**: **No**. Python's creator (Guido van Rossum) famously decided against it to keep stack traces clear for debugging. Deep recursion will always hit the stack limit in CPython.
14. **Q: What is the difference between an 'Iterable' and an 'Iterator'?**
    - **Answer**: An **Iterable** is the data source (like a List). An **Iterator** is the object that actually performs the iteration (`next()`).
15. **Q: How can you use `zip()` to transpose a matrix?**
    - **Answer**: `list(zip(*matrix))`.
16. **Q: What is the purpose of `operator.itemgetter`?**
    - **Answer**: It is a high-speed way to extract a specific field from a collection. It's often used as a `key` for sorting operations.
17. **Q: Explain 'Lazy Evaluation' in the context of `map()` or `filter()`.**
    - **Answer**: They don't process the data until you actually iterate through them. This allows you to process infinite streams of data without crashing the RAM.
18. **Q: Is a 'Lambda' faster than a 'Def' function?**
    - **Answer**: No. They are functionally identical in the CPython bytecode.
19. **Q: What is a 'Side Effect'?**
    - **Answer**: Any change an application makes to the world outside itself (e.g., writing to a file, changing a global variable, or printing to the console).
20. **Q: Why is Python not a 'Pure' functional language?**
    - **Answer**: Because it allows for mutable data structures (lists, dicts) and doesn't enforce side-effect-free programming. It is a "Multi-Paradigm" language.

---

[← Previous: OOP](08-object-oriented-programming.md) | [Next: Decorators →](10-decorators-context-managers.md)
