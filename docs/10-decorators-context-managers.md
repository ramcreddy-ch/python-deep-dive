# 10. Decorators & Context Managers — Clean & Reusable Logic

> "Decorators and Context Managers are the 'Wrapper' patterns of Python. They allow you to add powerful behavior (like logging, authentication, and error retries) to existing code without cluttering your core business logic."

---

## 🌱 The Basics: Context Managers (`with`)
A Context Manager ensures that a resource (file, database, network) is **cleaned up** even if your code crashes.

```python
# The 'with' statement handles opening and closing automatically
with open("test.txt", "w") as f:
    f.write("Safe writing!")
```

---

## 🌿 Intermediate: Simple Decorators
A decorator is a function that takes *another* function and adds behavior to it.

```python
def my_decorator(func):
    def wrapper():
        print("--- START ---")
        func()
        print("--- END ---")
    return wrapper

@my_decorator # Using the @ syntax
def hello():
    print("Hello world")

# hello()
```

---

## 🌳 Advanced: Professional Decorators (*args & **kwargs)
For real-world production, your decorator must work with functions that have any number of arguments.

**Real Use (DevOps/SRE)**:
A logging decorator that records every execution of an automation script.

```python
import functools

def log_execution(func):
    @functools.wraps(func) # Keeps the original function's name and docstring
    def wrapper(*args, **kwargs):
        print(f"Executing {func.__name__} with {args} {kwargs}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@log_execution
def scale_cluster(namespace, replicas=3):
    print(f"Scaling {namespace} to {replicas}")
```

---

## 🔥 Expert: Custom Context Managers (Class & Generator)
Principal engineers build their own resource managers to handle complex cloud or database locks.

### 1. The Generator Pattern (`@contextmanager`)
The simplest way to build a high-performance context manager.

```python
from contextlib import contextmanager

@contextmanager
def temporary_file_lock(filename):
    """
    Expert Pattern: Custom Lifecycle. 
    Demonstrates: Automating 'Setup' and 'Teardown' for production reliability.
    """
    print(f"SETTING LOCK ON {filename}")
    try:
        # This is where your code inside the 'with' block runs
        yield f"HANDLE TO {filename}"
    finally:
        # This code runs even if the 'with' block crashes!
        print(f"RELEASING LOCK ON {filename}")

# Usage
# with temporary_file_lock("db.sqlite") as lock:
#     print(f"Working on {lock}")
```

---

## 🎯 Top 20 Principal Interview Questions (Decorators & Context Managers)

1. **Q: What is a Decorator in Python?**
   - **Answer**: It is a 'Wrapper' function that allows you to add functionality to an existing function or class without modifying its source code.
2. **Q: Why use `@functools.wraps` inside a decorator?**
   - **Answer**: It preserves the original function's **Metadata** (like `__name__` and `__doc__`). Without it, your decorated function would appear as the internal `wrapper` function in tracebacks and documentation.
3. **Q: Explain the `__enter__` and `__exit__` methods.**
   - **Answer**: These are the methods that define a **Context Manager**. `__enter__` handles setup (opening a file); `__exit__` handles teardown (closing the file), even if an error occurs.
4. **Q: Can a decorator take its own arguments?**
   - **Answer**: Yes. This requires a "Nested" decorator structure: The top function takes the arguments, the second function takes the target function, and the third function is the wrapper.
5. **Q: What is a 'Class-Based' Decorator?**
   - **Answer**: A class that implements `__call__`. It can store state (like a counter) across multiple calls to the decorated function.
6. **Q: How can you decorate an entire Class?**
   - **Answer**: By applying the `@decorator` above the class definition. It takes the class as an argument and returns either the modified original class or a completely new one.
7. **Q: What is the `contextlib.contextmanager` decorator?**
   - **Answer**: It allows you to build a context manager using a **Generator** (`yield`) instead of a full class with `__enter__` and `__exit__`.
8. **Q: How do you handle 'Nested' Context Managers safely?**
   - **Answer**: You can nest `with` statements: `with open(A) as f1, open(B) as f2:`. Or use `contextlib.ExitStack` for a dynamic number of resources.
9. **Q: Can a decorator be used for 'Memoization'?**
   - **Answer**: Yes. It can store a dictionary of previous results and return them instantly if the inputs are the same (see `functools.lru_cache`).
10. **Q: What happens if an exception occurs inside the `__enter__` method?**
    - **Answer**: The code inside the `with` block **never runs**, and the `__exit__` method is **not called**.
11. **Q: What is the difference between `@property` and a standard decorator?**
    - **Answer**: `@property` is a built-in decorator that turns a method into a **Descriptor** (Getter/Setter/Deleter), allowing it to be accessed like an attribute.
12. **Q: Can you chain multiple decorators?**
    - **Answer**: Yes. They are applied **bottom-to-top**. The one closest to the function definition is applied first.
13. **Q: What is the `__exit__` method's return value used for?**
    - **Answer**: If it returns `True`, it **suppresses** any exception that occurred inside the `with` block. If it returns `False` (default), the exception propagates normally.
14. **Q: How do you decorate an 'Async' function?**
    - **Answer**: Your wrapper function must be defined as `async def wrapper()` and you must `await` the original function inside it.
15. **Q: What is a 'Singleton' pattern using a decorator?**
    - **Answer**: A decorator that wraps a class and ensures only **one** instance of it ever exists in the application.
16. **Q: How do you access the 'Original' function from a decorated one?**
    - **Answer**: If you used `@functools.wraps`, the original function is stored in the `__wrapped__` attribute.
17. **Q: What is the purpose of `contextlib.suppress`?**
    - **Answer**: A high-speed context manager for ignoring specific exceptions: `with suppress(FileNotFoundError):`.
18. **Q: Can a decorator be used for 'Role-Based Access Control'?**
    - **Answer**: Yes. A decorator can check the current user's permissions and raise an error if they aren't authorized to call that function.
19. **Q: What is the 'Registry' pattern with decorators?**
    - **Answer**: Using a decorator to "Save" a reference to functions in a list or dictionary (like how Flask registers routes).
20. **Q: What is a 'Mocking' decorator in tests?**
    - **Answer**: `unittest.mock.patch` is a decorator that replaces a real object with a mock for the duration of the test.

---

[← Previous: Functional Programming](09-functional-programming.md) | [Next: Generators & Iterators →](11-generators-iterators.md)
