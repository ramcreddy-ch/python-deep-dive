# 10. Decorators & Context Managers — Clean & Reusable logic

> "Decorators and Context Managers are the 'Wrapper' patterns of Python. They allow you to add powerful behavior (like logging, authentication, and error retries) to existing code without changing its source. An expert uses these to separate 'Business Logic' from 'Infrastructure Logic'."

---

## ❓ The 'Why' (High-Level)
In any professional application, you have "Cross-Cutting Concerns"—tasks that need to happen in many places (e.g., checking if a user is logged in, measuring execution time, or opening a database connection). If you copy-paste this logic into every function, your code becomes unreadable and fragile. **Decorators** allow you to "wrap" functions with this logic, and **Context Managers** allow you to "wrap" blocks of code. 

---

## 🌱 Module 1: The Basics (Junior) — The `@` Syntax
At its simplest, a decorator is just a function that takes a function and returns a modified version of it.

### 1. Basic Decorator
```python
def my_decorator(func):
    def wrapper():
        print("Something before...")
        func()
        print("Something after...")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")
```

### 2. The `with` Statement
Context Managers ensure that "Setup" and "Teardown" happen automatically.
```python
with open("file.txt") as f:
    # Setup happens (file opens)
    data = f.read()
# Teardown happens automatically (file closes)
```

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — Power Wrapping
Mid-level engineers write decorators that can handle arguments and preserve function identity.

### 1. Handling Arguments with `wraps`
Without `functools.wraps`, your decorated function "loses" its name and docstring.
```python
from functools import wraps

def debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

### 2. Decorators with Parameters
If you want to pass a value to the decorator itself (like `@retry(times=3)`), you need a "Triply-Nested" function.
```python
def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times): result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator
```

---

## 🌳 Module 3: Advanced Mechanics (Senior) — Custom Contexts
Senior engineers build their own resource-management protocols.

### 1. The `@contextmanager` Decorator
The simplest way to create a context manager without writing a full class.
```python
from contextlib import contextmanager

@contextmanager
def temp_database():
    print("Connecting...")
    db = "Connected"
    try:
        yield db  # This is the 'as' variable in the 'with' block
    finally:
        print("Disconnecting...")
```

### 2. Handling Exceptions in `__exit__`
When building a context manager class, you can choose to "swallow" or "propagate" an error that happens inside the block.

---

## 🔥 Module 4: Principal Architect (Principal) — Class Decorators
At the highest level, you use objects to manage stateful decoration.

### 1. State-Aware Class Decorators
Using a class allows the decorator to "remember" how many times it has been called or store configuration.
```python
class CallCounter:
    def __init__(self, func):
        self.func = func
        self.count = 0
    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)
```

### 2. Asynchronous Context Managers
For modern cloud apps, context managers must be `async` to handle network cleanup without blocking.
- **Protocol**: `__aenter__` and `__aexit__`.

---

## 🏗️ Case Study: The API Retry & Rate-Limiter
A fintech company was getting "Rate Limited" (Error 429) by an external bank API.
- **The Junior Approach**: Adding `try/except` and a `time.sleep(1)` inside every API call function.
- **The Principal Approach**: Built a single `@resilient_call` decorator that automatically handled retries, backoff timing, and error logging.
- **Result**: The team was able to apply this protection to **all 50** bank endpoints by simply adding one `@` line above each function name.

---

## ⚡ Anti-Patterns & Expert Traps

### 1. The "Magic" Trap
If you use too many decorators, your code becomes "Magical"—it's hard to tell what is actually happening. **Expert fix**: Use decorators only for generic infrastructure logic, not for business rules.

### 2. Forgetting `functools.wraps`
If you forget this, debugging becomes a nightmare because error tracebacks will point to the `wrapper` instead of the real function.

---

## 🎯 Top 20 Principal Interview Questions (Decorators & Context Managers)

1. **Q: What is a Decorator in Python?**
   - **Answer**: It's a high-order function that takes another function as an argument and extends its behavior without explicitly modifying its source code.
2. **Q: Explain the `@` syntax.**
   - **Answer**: It's "syntactic sugar" for `func = decorator(func)`. It must be placed immediately above the function definition.
3. **Q: Why is `functools.wraps` important?**
   - **Answer**: Because it copies the original function's **metadata** (name, docstring, and annotations) from the original function to the wrapper, making debugging and documentation tools work correctly.
4. **Q: How do you pass arguments to a decorator itself?**
   - **Answer**: By creating a "Decorator Factory"—a function that takes the arguments and returns the actual decorator function.
5. **Q: What is the difference between a Function Decorator and a Class Decorator?**
   - **Answer**: A function decorator wraps a function. A class decorator wraps a **Class Definition**, allowing you to modify how its objects are created or initialized.
6. **Q: What is a 'Context Manager'?**
   - **Answer**: An object that defines the runtime context to be established when executing a `with` statement. It ensures that resources are allocated and released cleanly.
7. **Q: Explain the `__enter__` and `__exit__` methods.**
   - **Answer**: `__enter__` runs at the start of the `with` block and returns the resource. `__exit__` runs at the end, even if an error occurred, to perform cleanup.
8. **Q: What is the `contextlib` module?**
   - **Answer**: A standard library module that provides utilities for working with context managers, most notably the `@contextmanager` decorator for creating them using a single generator.
9. **Q: How do you handle an exception inside a custom Context Manager?**
   - **Answer**: The `__exit__` method receives the exception type, value, and traceback as arguments. If `__exit__` returns `True`, the exception is "swallowed"; if it returns `False` (or None), the exception propagates.
10. **Q: What is an 'Asynchronous Context Manager'?**
    - **Answer**: Introduced in 3.5, it implements `__aenter__` and `__aexit__` instead of the synchronous versions. It is used with `async with` for non-blocking I/O cleanup.
11. **Q: Can one function have multiple decorators?**
    - **Answer**: Yes. They are applied from the **Bottom Up** (the one closest to the function runs first, and its result is passed to the one above it).
12. **Q: What is the `yield` keyword's role in `@contextmanager`?**
    - **Answer**: It separates the "Setup" code (everything before `yield`) from the "Teardown" code (everything after `yield`).
13. **Q: Can a decorator be used for something other than functions and classes?**
    - **Answer**: In Python, decorators can also be applied to **Methods** inside a class.
14. **Q: What is 'Mojo' or 'Monkey Patching' in decorators?**
    - **Answer**: Using a decorator to dynamically replace a function or class at runtime with a different version, often used in testing to mock out external APIs.
15. **Q: Explain how to write a decorator that works on both functions and methods.**
    - **Answer**: You must account for the `self` or `cls` argument that is automatically passed to methods. Using `*args` and `**kwargs` usually handles this seamlessly.
16. **Q: What is the purpose of `contextlib.ExitStack`?**
    - **Answer**: It allows you to enter a **Dynamic number** of context managers simultaneously, ensuring they are all closed correctly.
17. **Q: How do you implement a 'Singleton' using a decorator?**
    - **Answer**: By creating a decorator that stores an instance of a class in a local dictionary and returns it every time the class is "called" (instantiated).
18. **Q: What happens if a decorator doesn't return the wrapper function?**
    - **Answer**: The original function will be replaced by `None` (or whatever else the decorator returns), and attempting to call it will result in a `TypeError`.
19. **Q: Can a class be used as a context manager and a decorator simultaneously?**
    - **Answer**: Yes, by implementing `__enter__`, `__exit__`, and `__call__` in the same class.
20. **Q: What is 'Parametric Error Handling' in context managers?**
    - **Answer**: Using a context manager to decide whether to catch or log certain types of errors based on parameters passed to the manager (e.g., `with ignore_errors(IOError):`).

---

[Previous: Functional Programming](09-functional-programming.md) | [Next: Generators & Iterators →](11-generators-iterators.md)
