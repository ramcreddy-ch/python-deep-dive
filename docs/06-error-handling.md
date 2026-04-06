# 06. Error Handling & Resilience — Failures, Context & Tracebacks

> "In production, code doesn't just run; it fails. An expert doesn't just 'fix' bugs; they build systems that handle failure gracefully, log correctly, and recover automatically without manual intervention. Mastering error handling is the difference between an 'App' and a 'Service'."

---

## ❓ The 'Why' (High-Level)
Failures are inevitable: network timeouts, malformed user input, or missing database rows. If your code isn't prepared, it crashes, causing downtime and lost revenue. A principal engineer designs for **Resilience**, ensuring that a single error in a non-critical component (like a logger) doesn't bring down the entire payment gateway.

---

## 🌱 Module 1: The Basics (Junior) — The Core Catch
To stop a crash, you must "catch" the error before it hits the operating system.

### 1. The `try-except` Block
This is the basic safety net.
```python
try:
    x = 10 / 0
except ZeroDivisionError:
    print("You can't divide by zero!")
```

### 2. Common Exception Types
- **ValueError**: Right type, wrong value (e.g., `int("abc")`).
- **TypeError**: Wrong operation for the type (e.g., `5 + "10"`).
- **IndexError**: Trying to access a list index that doesn't exist.

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — Clean Cleanup
Mid-level engineers ensure that resources (like open files) are always closed, even if an error occurs.

### 1. `finally` and `else`
- **`finally`**: Code that runs **no matter what** (good for closing files).
- **`else`**: Code that runs **only if no error occurred**.
```python
try:
    f = open("data.txt")
except FileNotFoundError:
    print("File missing!")
else:
    print("File read successfully!")
finally:
    f.close()  # Guaranteed to run.
```

### 2. Custom Exceptions
Don't use generic `ValueError` for everything. Create your own for business logic.
```python
class InsufficientFundsError(Exception):
    """Raised when a user tries to withdraw more than their balance."""
    pass

def withdraw(amount, balance):
    if amount > balance:
        raise InsufficientFundsError(f"Needed {amount}, but only had {balance}")
```

---

## 🌳 Module 3: Advanced Mechanics (Senior) — Context Managers
Senior engineers use the **`with` statement** (The Context Manager protocol) to automate resource management.

### 1. The `with` Statement
Instead of `finally: f.close()`, just use `with`:
```python
with open("data.txt") as f:
    data = f.read()
# File is automatically closed here, even if f.read() crashes!
```

### 2. Exception Chaining
Sometimes you want to catch one error and raise a different one, but keep the "History" of the original.
```python
try:
    db.save(data)
except DatabaseError as e:
    # 'from e' attaches the original traceback to the new one!
    raise APIError("Failed to process transaction") from e
```

---

## 🔥 Module 4: Principal Architect (Principal) — Resilient Systems
At the highest level, you handle **Multiple concurrent errors** and optimize for the "Happy Path."

### 1. Exception Groups (Python 3.11+)
In modern async systems, multiple tasks might fail at once. Python uses `ExceptionGroup` and the `except*` syntax to catch them.
```python
# python 3.11+
try:
    run_complex_tasks()
except* ValueError as eg:
    handle_value_errors(eg)
except* NetworkError as eg:
    retry_network(eg)
```

### 2. The Cost of Exceptions
Python's `try/except` block is **Zero-Cost** in modern versions if no error happens. However, when an error *is* raised, generating the **Traceback object** is expensive.
- **Principal Advice**: Never use Exceptions for "Expected" control flow (like checking if a file exists). Use an `if` check instead.

---

## 🏗️ Case Study: The Self-Healing API
A global streaming service was losing 1% of traffic due to intermittent network "blips" during API calls.
- **The Junior Approach**: Add `try-except` and log the error. (User still sees a failure).
- **The Principal Approach**: Built a **Retry Wrapper** using the `tenacity` library. It caught specific `NetworkError` types and automatically retried the request with "Exponential Backoff" (waiting 1s, then 2s, then 4s).
- **Result**: API success rate increased from 99% to 99.99%, saving the company millions in customer support calls.

---

## ⚡ Anti-Patterns & Expert Traps

### 1. The Bare `except:`
**NEVER** do this: `except: pass`. It swallows every error, including keyboard interrupts (Ctrl+C) and system errors, making it impossible to debug.
- **Expert Fix**: Always catch a specific class: `except Exception:`.

### 2. Silencing Errors with `pass`
If you catch an error and do nothing, you are hiding a problem that will likely cause a bigger crash later. **Always log** or re-raise.

### 3. Deep Nesting in Try Blocks
Keep your `try` blocks as **small** as possible to avoid catching an error you didn't expect.

---

## 🎯 Top 20 Principal Interview Questions (Error Handling)

1. **Q: What is the difference between a 'Syntax Error' and an 'Exception'?**
   - **Answer**: A **Syntax Error** happens while the code is being parsed (before it even runs). An **Exception** occurs while the code is already running (e.g., a division by zero).
2. **Q: Why is a bare `except:` clause considered dangerous?**
   - **Answer**: It catches **every** error, including system exits like `SystemExit` or `KeyboardInterrupt`. This makes it impossible to stop a running script and hides bugs that should be fixed.
3. **Q: Explain the purpose of the `finally` block.**
   - **Answer**: It defines code that **must** run, regardless of whether an error occurred or was caught. It's the standard place for cleanup tasks like closing database connections.
4. **Q: What is the `else` block used for in a `try/except` statement?**
   - **Answer**: It runs only if the code in the `try` block **did not raise an exception**. It's useful for logic that should only happen after a successful operation.
5. **Q: What is the proper way to manually raise an exception?**
   - **Answer**: Using the `raise` keyword, followed by an exception instance: `raise ValueError("Invalid entry")`.
6. **Q: What is 'Exception Chaining' and why is it useful?**
   - **Answer**: The industry practice of catching one exception and raising another while preserving the original traceback using `raise NewError() from original_error`. This provides a complete "audit trail" of the failure.
7. **Q: Explain the 'Context Manager' protocol.**
   - **Answer**: It's a set of methods (`__enter__` and `__exit__`) that allow objects to manage resources automatically within a `with` statement.
8. **Q: What is the difference between `Exception` and `BaseException`?**
   - **Answer**: `BaseException` is the root of all exceptions. `Exception` is the parent of all **Standard** errors. System-level exits (`KeyboardInterrupt`, `SystemExit`) inherit from `BaseException` but NOT from `Exception`.
9. **Q: How can you access the details of an exception object in an `except` block?**
   - **Answer**: By using the `as` keyword: `except ValueError as e:`. You can then access its message using `str(e)` or its arguments using `e.args`.
10. **Q: What is a 'Traceback' and how can you print it manually?**
    - **Answer**: A list showing the chain of function calls that led to an error. You can print it using the `traceback` module: `traceback.print_exc()`.
11. **Q: How does the `with` statement simplify error handling?**
    - **Answer**: It ensures that resources are **cleanly released** (using the `__exit__` method) as soon as the block ends, even if an error is raised inside the block.
12. **Q: What is the `assert` statement used for?**
    - **Answer**: for **Development-time debugging**. It checks if a condition is True and raises an `AssertionError` if not. Note: `assert` is often removed in production (`python -O`).
13. **Q: Can you catch multiple exceptions in a single `except` block?**
    - **Answer**: Yes, by passing them as a tuple: `except (ValueError, TypeError):`.
14. **Q: What are 'Exception Groups' (introduced in Python 3.11)?**
    - **Answer**: They allow a single exception to contain **multiple nested exceptions**. This is useful in asynchronous programming when multiple tasks fail simultaneously.
15. **Q: Explain the 'Look Before You Leap' (LBYL) vs 'Easier to Ask for Forgiveness' (EAFP) styles.**
    - **Answer**: **LBYL**: Checking if a file exists before opening it (`if os.path.exists`). **EAFP**: Trying to open the file and catching the `FileNotFoundError`. Python strongly prefers **EAFP**.
16. **Q: What happens if an exception is raised inside a `finally` block?**
    - **Answer**: The original exception (if any) is lost, and the new exception from the `finally` block propagates upward. This is a common source of bugs.
17. **Q: How do you define a custom exception class?**
    - **Answer**: By creating a class that inherits from the built-in `Exception` class: `class MyError(Exception): pass`.
18. **Q: What is the `StopIteration` exception used for?**
    - **Answer**: internally by iterators and `for` loops to signal that there are no more items to be produced.
19. **Q: Why should you avoid using Exceptions for normal program flow control?**
    - **Answer**: Because raising an exception is **Performance-heavy** (building the traceback) and it makes the code's logic harder to follow.
20. **Q: What is the `sys.exc_info()` function?**
    - **Answer**: A built-in function that returns a tuple about the current exception being handled (Type, Value, Traceback). It's used for deep-level debugging and custom logging.

---

[Previous: Data Structures](05-data-structures.md) | [Next: File I/O →](07-file-io-serialization.md)
