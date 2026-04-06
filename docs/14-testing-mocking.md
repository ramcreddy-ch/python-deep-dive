# 14. Testing & Mocking — Pytest, Mocks & Test-Driven Development

> "Code without tests isn't finished; it's a liability. An expert doesn't just test the 'Happy Path'; they use Mocks to isolate components and Property-Based testing to find edge cases that a human would never think of. High-quality tests are what allow a system to be refactored safely 10 years after it was written."

---

## ❓ The 'Why' (High-Level)
If you change a line of code in a large system, how do you know you didn't break 5 other things you weren't even thinking about? Without **Automated Testing**, you are just guessing. A principal engineer knows that tests are **Insurance**. The time you spend writing tests today is paid back 10x over by preventing production outages and "Regression" bugs later.

---

## 🌱 Module 1: The Basics (Junior) — The `unittest` Framework
Testing is just writing code that calls your code and checks the result.

### 1. Basic Assertions
The simplest test is an `assert`.
```python
def add(a, b): return a + b
assert add(2, 2) == 4
```

### 2. Standard `unittest`
Python's built-in framework for organized testing.
```python
import unittest

class TestMath(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(add(2, 2), 4)
```

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — The Power of `pytest`
Professional Python developers almost exclusively use **`pytest`**. It's more readable and powerful.

### 1. Simple Syntax
No need for classes or `self.assertEqual`. Just use standard Python `assert`.

### 2. Fixtures: The Smart Setup
A **Fixture** is a function that provides reliable input for your tests (e.g., a test database connection).
```python
import pytest

@pytest.fixture
def test_user():
    return {"id": 1, "name": "Test"}

def test_login(test_user):
    # 'test_user' is automatically injected into this function!
    assert test_user["id"] == 1
```

---

## 🌳 Module 3: Advanced Mechanics (Senior) — Mocking & Isolation
Senior engineers don't test "The Whole World" at once. They use **Mocks** to isolate the code being tested.

### 1. What is a Mock?
A Mock is a "Fake" object that replaces a slow or complex dependency (like a database or a network API).
```python
from unittest.mock import Mock

database = Mock()
database.get_user.return_value = {"id": 1, "name": "Ram"}

# Now your test can run without a real database!
```

### 2. The `patch` Decorator
Allows you to temporarily replace a function or class inside your module during a test.
```python
@patch("module.requests.get")
def test_api_call(mock_get):
    mock_get.return_value.status_code = 200
    ...
```

---

## 🔥 Module 4: Principal Architect (Principal) — TDD & Advanced Protocols
At the highest level, the test **defines the architecture**.

### 1. Test-Driven Development (TDD)
- **Red**: Write a failing test for a feature that doesn't exist yet.
- **Green**: Write the minimum code to make the test pass.
- **Refactor**: Clean up the code while keeping the test Green.

### 2. Property-Based Testing
Instead of testing specific numbers like `2+2`, you test **Properties** that must always be true.
- **Tool**: `Hypothesis`.
- **Logic**: "For **any** two integers $a$ and $b$, $a+b$ must equal $b+a$." Hypothesis will try thousands of random numbers (including negatives, zero, and huge integers) to find a way to break your code.

---

## 🏗️ Case Study: The Zero-Downtime Migration
A fintech firm needed to rewrite their currency conversion logic.
- **The Junior Approach**: Rewrite the code, manually check a few conversions, and deploy. (Result: rounding errors caused thousands of dollars in loss).
- **The Principal Approach**: Used **Mocking** to isolate the core logic and wrote **Parameterized Tests** for 1,000 different currency pairs. They then ran a "Parallel Run" where the old and new systems processed the same data to ensure the results were identical.
- **Result**: Successfully deployed the new engine with **zero** bugs reported in production.

---

## ⚡ Anti-Patterns & Expert Traps

### 1. Testing Implementation, Not Behavior
If you test "How" a function works (internal variables) rather than "What" it returns, your tests will break every time you refactor, even if the code is correct. **Expert fix**: Only test inputs and outputs.

### 2. The Slow Test Suite
If your tests take 20 minutes to run, developers will stop running them. Use **Mocks** to replace slow I/O and keep your unit tests running in under 5 seconds.

---

## 🎯 Top 20 Principal Interview Questions (Testing & Mocking)

1. **Q: What is the difference between Unit Testing and Integration Testing?**
   - **Answer**: **Unit Testing** tests a single part of the code (like one function) in isolation. **Integration Testing** tests how multiple parts of the system work together (e.g., function + database).
2. **Q: Why is `pytest` generally preferred over `unittest`?**
   - **Answer**: It is less verbose, supports high-power **Fixtures**, and has a massive ecosystem of plugins (like `pytest-cov`, `pytest-xdist`, `pytest-asyncio`).
3. **Q: What is a 'Mock' object?**
   - **Answer**: A simulated object that mimics the behavior of a real dependency (like an external API) in a controlled way, allowing the test to remain fast and predictable.
4. **Q: Explain 'Monkey Patching' in the context of testing.**
   - **Answer**: The process of dynamically replacing a function or class at runtime (using `patch`) so that the code under test uses a Mock instead of the real dependency.
5. **Q: What is 'Test Coverage'?**
   - **Answer**: A metric (usually a percentage) that shows how much of your source code was actually executed during the test run. While 100% is a good goal, high coverage doesn't guarantee lack of bugs.
6. **Q: What are 'Fixtures' in `pytest`?**
   - **Answer**: Functions that provide data or state (like a temporary file or a dummy user) to tests. They use **Dependency Injection**, meaning the test function just asks for them as arguments.
7. **Q: Explain 'Parameterized Testing'.**
   - **Answer**: A technique to run the **Same Test** multiple times with different sets of inputs and expected outputs, reducing code duplication.
8. **Q: What is the purpose of `unittest.mock.MagicMock`?**
   - **Answer**: It is a subclass of `Mock` that has pre-defined default behaviors for all "Magic" (dunder) methods, like `__len__`, `__getitem__`, and `__iter__`.
9. **Q: What is 'Property-based Testing'?**
   - **Answer**: A testing style (e.g., using `Hypothesis`) where you define **General Rules** about your code's behavior rather than specific examples, and the library tries to find edge cases that break those rules.
10. **Q: What is 'TDD' (Test-Driven Development)?**
    - **Answer**: A software development process where you write the **Test First** (Red), then the code (Green), and then clean it up (Refactor).
11. **Q: How do you mock an async function correctly?**
    - **Answer**: In modern Python (3.8+), `AsyncMock` is used. It correctly implements the awaitable protocol so that `await my_mock()` works as expected.
12. **Q: Explain 'Side Effect' in a Mock.**
    - **Answer**: A way to make a mock **raise an exception** or return different values on different calls: `mock.side_effect = [1, 2, ValueError]`.
13. **Q: What is the difference between `patch()` and `patch.object()`?**
    - **Answer**: `patch()` is used when you have a string path to a module. `patch.object()` is used when you already have a reference to the object or class you want to mock.
14. **Q: What is 'Smoke Testing'?**
    - **Answer**: Simple, high-level tests that check if a system "Starts up" and basic features work, without testing every deep edge case.
15. **Q: How do you test that a function raises a specific exception?**
    - **Answer**: In `pytest`, use the `with pytest.raises(ExceptionType):` context manager.
16. **Q: What is the 'Arrange-Act-Assert' pattern?**
    - **Answer**: The standard structure for a clean test: 1. **Arrange** the data. 2. **Act** (call the function). 3. **Assert** the result matches expectations.
17. **Q: What is 'Flaky Test' and how do you handle it?**
    - **Answer**: A test that passes sometimes and fails sometimes without any code changes (often due to race conditions or external network dependence). The only solution is to fix the underlying non-determinism.
18. **Q: What is 'Refactoring' in the TDD cycle?**
    - **Answer**: Improving the **Internal Design** of the code (making it cleaner/faster) without changing its external behavior, as verified by existing tests.
19. **Q: What is the purpose of `pytest.mark.skip`?**
    - **Answer**: To tell the test runner to ignore a specific test temporarily, often because it's a known bug or only works on a different OS.
20. **Q: Can you test 'Private' methods?**
    - **Answer**: Technically yes, but **you shouldn't**. Testing private methods makes your tests fragile. If a private method is complex enough to need its own tests, it probably should be a separate public class or function.

---

[Previous: AsyncIO](13-asyncio-concurrency.md) | [Next: Networking & HTTP/2 →](15-networking-http.md)
