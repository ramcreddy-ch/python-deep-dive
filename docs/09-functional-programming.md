# 09. Functional Programming — Lambda, Map, Filter & Immutability

> "Functional programming isn't about functions; it's about avoiding 'Side Effects' and treating data as a 'Transformation'. An expert uses functional patterns to build clean, predictable systems that are significantly easier to test and scale."

---

## ❓ The 'Why' (High-Level)
In standard programming, we often change (mutate) variables. But in a massive system with 100 threads, mutation leads to **Race Conditions** and bugs that are impossible to find. **Functional Programming (FP)** treats data as "Immutable" (unchanging). Instead of changing a list, you create a *new* list that represents the change. This leads to code that is **Stateless** and much easier to parallelize.

---

## 🌱 Module 1: The Basics (Junior) — Pure Functions
A **Pure Function** is one that always returns the same output for the same input and doesn't change anything outside itself (no side effects).

### 1. The Core Trinity: Map, Filter, Reduce
- **Map**: Apply a function to every item.
- **Filter**: Keep only items that meet a condition.
- **Reduce**: Combine all items into one (e.g., a total).
```python
nums = [1, 2, 3, 4]
# Junior: For loop
# Mid-Level: List Comprehension
# Expert: functional map
squared = list(map(lambda x: x*x, nums))
```

### 2. Lambdas (Anonymous Functions)
Lambdas are one-line, nameless functions. Use them only when the logic is very simple.

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — Functools
To move to mid-level, you must stop rewriting logic and start "Configuring" it.

### 1. `functools.partial`
Allows you to "Pre-fill" some arguments of a function to create a specialized version of it.
```python
from functools import partial

def power(base, exp): return base ** exp

square = partial(power, exp=2)
cube = partial(power, exp=3)
print(square(10))  # 100
```

### 2. List Comprehensions (The Pythonic FP)
Comprehensions are almost always faster and more readable than `map` and `filter` in Python.
- **`[x*x for x in nums if x > 0]`** instead of `list(map(..., filter(..., nums)))`.

---

## 🌳 Module 3: Advanced Mechanics (Senior) — Itertools & Cache
Senior engineers use memory-efficient tools for infinite or massive data.

### 1. The `itertools` Library (Lazy Iteration)
`itertools` generates values **on demand** rather than storing them in RAM.
- **`chain()`**: Combine multiple lists without copying them.
- **`product()`**: Generate a Cartesian product (nested loops in 1 line).

### 2. `functools.lru_cache` (Memoization)
Automatically memorize the output of a slow function so you don't have to calculate it twice.
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def slow_math(n):
    # This result is saved 'cached' for future calls!
    return n * n 
```

---

## 🔥 Module 4: Principal Architect (Principal) — Declarative Pipelines
At the highest level, you treat your software as a "Pipeline" of state-free transformations.

### 1. The Single Dispatcher
In languages like Java, you can "Overload" a function with different types. In Python, we use `@singledispatch`.
```python
from functools import singledispatch

@singledispatch
def process(data): print("Handling generic data")

@process.register(dict)
def _(data): print("Handling a dictionary")
```

### 2. Immutability at Scale
Using **`frozenset`** or **`namedtuple`** ensures that your data objects cannot be accidentally modified by a different part of the system. This makes debugging massive distributed systems a breeze.

---

## 🏗️ Case Study: The 100-Million Row Transformer
A data engineering team needed to transform 100 million sensor records.
- **The Junior Approach**: Load into a list, loop over it. (Server crashed with Out-of-Memory).
- **The Principal Approach**: Used **Generators** and **`itertools.chain`** to "Stream" the data. The data was read 1 row at a time, transformed, and written to the output file immediately.
- **Result**: Reduced memory usage from 64GB to **20MB**, and the process ran 40% faster.

---

## ⚡ Anti-Patterns & Expert Traps

### 1. Over-Lambda-ing
If your lambda function is more than 50 characters long, **Stop!** Write a regular `def` function. Lambdas are harder to test and debug because they have no name in a traceback.

### 2. Recursion in Python
Python's standard recursion limit is 1,000. Unlike Haskell or Scala, Python does not have "Tail Call Optimization." Never use deep recursion for production data; use a `while` loop or a stack instead.

---

## 🎯 Top 20 Principal Interview Questions (Functional Programming)

1. **Q: What is a 'Pure Function'?**
   - **Answer**: it is a function that returns the same output for the same input and has **No Side Effects** (does not change external state or perform I/O).
2. **Q: Explain 'Immutability'.**
   - **Answer**: The concept that once an object is created, its state cannot be changed. Immutable objects (like tuples or strings) are safer to share between threads and easier to reason about.
3. **Q: What is a 'Lambda' function?**
   - **Answer**: It's a small, anonymous, one-line function that can take arguments and return an expression. It's used for short operations where defining a full function is overkill.
4. **Q: Explain 'Map', 'Filter', and 'Reduce'.**
   - **Answer**: **Map**: Transforms every item in a list. **Filter**: Removes items that don't match a condition. **Reduce**: (from `functools`) Accumulates items into a single result (e.g., sum).
5. **Q: Why are List Comprehensions often preferred over `map()`?**
   - **Answer**: They are more **Pythonic**, arguably more readable, and they allow for both mapping and filtering in a single, high-performance line of code.
6. **Q: What is `functools.partial`?**
   - **Answer**: It allows you to "Freeze" or "Pre-set" some arguments of a function, creating a new function that takes fewer arguments. This is useful for "Specializing" generic functions.
7. **Q: What is 'Lazy Evaluation'?**
   - **Answer**: The strategy where an expression is not evaluated until its result is needed. Objects from `itertools` and `range()` use this to save massive amounts of RAM.
8. **Q: What is `functools.lru_cache` and when should you use it?**
   - **Answer**: It is a 'Least Recently Used' **Cache**. It saves the results of function calls to avoid re-calculating them. Use it for **Expensive, pure functions** that are called with the same inputs frequently.
9. **Q: Explain the `itertools` module.**
   - **Answer**: A library of "Iterator Building Blocks." It provides high-speed, memory-efficient tools for infinite sequences, permutations, and combining collections without making copies.
10. **Q: What is the 'Recursion Limit'?**
    - **Answer**: By default, CPython limits recursion to **1,000 depth** to prevent stack overflow. It can be checked/changed via `sys.getrecursionlimit()`.
11. **Q: Does Python have Tail Call Optimization (TCO)?**
    - **Answer**: **No**. This means every recursive step consumes a stack frame, which is why iteration is generally preferred for deep calculations in Python.
12. **Q: What is 'First-Class Functions'?**
    - **Answer**: The ability of a language to treat functions as values—meaning they can be passed as arguments, returned, and stored in variables.
13. **Q: What is a 'Higher-Order Function'?**
    - **Answer**: A function that either **accepts another function** as an input or **returns a function** as its output.
14. **Q: Explain `functools.singledispatch`.**
    - **Answer**: it provides a way to implement **Generic Functions** (function overloading). You define a base function and then register different versions for different types (e.g., int, str, dict).
15. **Q: What is the difference between `itertools.zip_longest()` and built-in `zip()`?**
    - **Answer**: `zip()` stops when the shortest list runs out. `itertools.zip_longest()` continues until the longest list is finished, using a `fillvalue` for the shorter ones.
16. **Q: What is the benefit of using `frozenset` in an FP context?**
    - **Answer**: Because it is immutable, it is **Hashable**, allowing it to be used as a dictionary key or an item in another set.
17. **Q: Explain 'Side Effects' and why FP seeks to avoid them.**
    - **Answer**: A side effect is anything that changes external state (writing to a file, changing a global variable). FP avoids them to make code **Deterministic** and easier to debug.
18. **Q: What is the purpose of `itertools.chain()`?**
    - **Answer**: It allows you to loop over multiple lists as if they were a single list, but without the high memory cost of actually concatenating them.
19. **Q: What is 'Declarative' vs 'Imperative' programming?**
    - **Answer**: **Imperative**: Telling the computer *how* to do a task (loops, state). **Declarative**: Describing *what* you want (Functional pipelines, SQL queries).
20. **Q: How does `map()` behave in Python 3 vs Python 2?**
    - **Answer**: In Python 2, it returned a **List**. In Python 3, it returns an **Iterator** (Lazy evaluation), which is much more memory efficient.

---

[Previous: Object-Oriented Programming](08-object-oriented-programming.md) | [Next: Decorators & Context Managers →](10-decorators-context-managers.md)
