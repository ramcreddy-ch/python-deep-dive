# 06. Error Handling & Debugging — Exceptions, Context & Resilience

> "In production, code doesn't just run; it fails. An expert doesn't just 'fix' bugs; they build systems that handle failure gracefully, log correctly, and recover automatically without human intervention."

---

## 🌱 The Basics: Try-Except
Entry-level error handling allows your program to "ignore" a crash and continue.

- **try**: The code you expect might fail.
- **except**: What to do if it fails.
- **finally**: Code that runs NO MATTER WHAT (e.g., closing a file).

```python
try:
    with open("config.json") as f:
        data = f.read()
except FileNotFoundError:
    print("Config file not found! Using defaults.")
finally:
    print("Execution complete.")
```

---

## 🌿 Intermediate: Raising Exceptions
Don't just catch errors; **Throw them** (Raise) when your logic detects a problem.

**Expert Rule**:
Always raise specific exceptions (e.g., `ValueError`) rather than the generic `Exception`.

```python
def set_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative!")
    print(f"Age set to {age}")
```

---

## 🌳 Advanced: Custom Exception Hierarchies
Professional libraries create their own exception "Tree" to make debugging easier for their users.

**Real Use (API/Platform)**:
A custom error for an internal API client.

```python
class AppError(Exception):
    """Base class for all app errors."""
    pass

class APIConnectionError(AppError):
    """Raised when the backend API is unreachable."""
    pass

# Usage
# raise APIConnectionError("Timeout after 3 retries")
```

---

## 🔥 Expert: Resilience & Retry (Exponential Backoff)
For principal engineering, "Error Handling" means building a system that doesn't quit. 

### 1. The Retry Pattern
If a Cloud API call fails due to a temporary network blip, don't crash. **Wait and try again.**

### 2. Exponential Backoff
Wait 1s, then 2s, then 4s, then 8s. This prevents "Hammering" a failing server and gives it time to recover.

```python
import time
import random

def call_api_with_retry(attempts=3):
    """
    Expert Pattern: Exponential Backoff. 
    Demonstrates: Building a resilient automation script.
    """
    for i in range(attempts):
        try:
            # Simulate a flakey API
            if random.random() < 0.7:
                raise ConnectionError("Service Unavailable")
            return "SUCCESS"
        except ConnectionError as e:
            wait_time = 2**i # 1, 2, 4 seconds
            print(f"Attempt {i+1} failed ({e}). Retrying in {wait_time}s...")
            time.sleep(wait_time)
            
    raise Exception("Max retries exceeded!")
```

---

## 🎯 Top 20 Principal Interview Questions (Error Handling)

1. **Q: What is the difference between `raise e` and `raise from e`?**
   - **Answer**: `raise e` throws the exception as if it just happened. `raise from e` (Exception Chaining) explicitly links the new error to the original one. This allows a developer to see the full "Cause Chain" in the traceback, which is essential for debugging complex microservices.
2. **Q: Why is 'Silent Failure' (using an empty `except: pass`) dangerous?**
   - **Answer**: It suppresses the error without logging it. If a database connection fails, the app might continue running with "None" data, causing much harder-to-find bugs later in the execution. Always at least log the error or catch a specific exception.
3. **Q: What is the purpose of the `finally` block?**
   - **Answer**: It is used to define "Cleanup" actions that must run regardless of whether an error occurred or not (e.g., closing a network socket or a database connection).
4. **Q: What is the `else` block in a `try/except` used for?**
   - **Answer**: It runs ONLY if **no** exception was raised. It's useful for logic that should only proceed if the `try` block was successful, separating the "Success" path from the "Error" path.
5. **Q: How do you create a Custom Exception?**
   - **Answer**: By creating a class that inherits from the built-in `Exception` class. This allows you to catch specific business errors separately from general system errors.
6. **Q: What is the MRO of Exceptions?**
   - **Answer**: Exceptions are organized in a hierarchy. Catching `Exception` will catch almost everything. Catching `BaseException` will even catch things like KeyboardInterrupt (Ctrl+C), which is usually not desired.
7. **Q: Explain 'Assertion' in Python.**
   - **Answer**: Using `assert condition, "Error Message"`. It is used for internal sanity checks during development. Note: Assertions can be disabled in production using the `-O` flag, so never use them for critical business logic.
8. **Q: How do you handle multiple exceptions in a single `except` block?**
   - **Answer**: Use a tuple: `except (TypeError, ValueError):`.
9. **Q: What is the `traceback` module used for?**
   - **Answer**: It allows you to programmatically extract and print the full call stack when an error occurs, which is essential for logging errors to a file or a database.
10. **Q: What is the 'Retry' pattern with 'Exponential Backoff'?**
    - **Answer**: A strategy where you retry a failed operation (like a network call) after waiting for an increasing amount of time (1s, 2s, 4s, 8s). It avoids overloading a recovering service.
11. **Q: How do you log an error with the full traceback included?**
    - **Answer**: Use `logging.error("Message", exc_info=True)`.
12. **Q: What is the difference between `SystemExit` and `KeyboardInterrupt`?**
    - **Answer**: `SystemExit` is raised when `sys.exit()` is called. `KeyboardInterrupt` is raised when the user presses Ctrl+C. Both inherit from `BaseException`, not `Exception`.
13. **Q: Can you catch a `SyntaxError`?**
    - **Answer**: No, not within the same script that contains it. A `SyntaxError` occurs during the **Parsing** phase, before the code ever starts running. You can only catch it if you are using `exec()` or `eval()` on external code.
14. **Q: What is the purpose of `raise` without any arguments?**
    - **Answer**: It **Re-raises** the last active exception. It's used when you want to log an error but still let the calling function handle it.
15. **Q: What is 'EAFP' vs 'LBYL'?**
    - **Answer**: **EAFP** (Easier to Ask for Forgiveness than Permission) — just try the action and catch the error. **LBYL** (Look Before You Leap) — check if the file exists before trying to open it. Python strongly prefers EAFP.
16. **Q: What is an 'Exception Context'?**
    - **Answer**: When one exception is raised while handling another, the original exception is stored in the `__context__` attribute of the new one.
17. **Q: How do you access the error message inside an `except` block?**
    - **Answer**: Use `as`: `except ValueError as e: print(str(e))`.
18. **Q: What happens if a `finally` block contains a `return` statement?**
    - **Answer**: The `finally` block's return will **Overwrite** any return from the `try` or `except` blocks. This is a common "Gotcha" in advanced interviews.
19. **Q: What is the purpose of `unittest.mock.side_effect`?**
    - **Answer**: during testing, it allows a Mock object to **Raise an Exception** when called, simulating a failure in an external service.
20. **Q: What is the difference between a 'Warning' and an 'Exception'?**
    - **Answer**: Warnings don't stop the program. They are used to alert the developer to potential future problems (like a deprecated function). Exceptions are "Hard" errors that stop execution unless caught.

---

[← Previous: Data Structures](05-data-structures.md) | [Next: Level 2 Recap →](../Level-2/07-file-io-serialization.md)
