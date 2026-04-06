# 14. Testing & Mocking — Pytest, Fixtures & Isolation

> "Code that isn't tested is legacy code the moment it's written. An expert doesn't just 'test' their code; they build a 'Safety Net' of automated validation that allows them to refactor and deploy 100x a day with 100% confidence."

---

## 🌱 The Basics: Assertions & Unit Tests
A **Unit Test** checks a single function in isolation.

```python
def add(a, b): return a + b

# Basic Test
def test_add_success():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
```

---

## 🌿 Intermediate: Pytest Fixtures
A **Fixture** is a reusable piece of 'Setup' code that your tests can request.

**Real Use (Platform/Database)**:
Creating a temporary database connection that is shared by all tests in a file.

```python
import pytest

@pytest.fixture
def sample_user():
    """
    Expert Pattern: Setup/Teardown. 
    Demonstrates: Clean, isolated test data.
    """
    return {"id": 1, "name": "Alice", "role": "ADMIN"}

def test_user_permissions(sample_user):
    assert sample_user["role"] == "ADMIN"
```

---

## 🌳 Advanced: Mocking & Patching
To test a function that calls a real API (like AWS or Stripe), you must **Mock** the response. This ensures your tests are fast, free, and don't require an internet connection.

```python
from unittest.mock import patch

def get_cloud_status():
    # Imagine this hits a real AWS API...
    return "ONLINE"

def test_cloud_logic():
    with patch("__main__.get_cloud_status") as mock_status:
        # 1. Fake the return value
        mock_status.return_value = "MAINTENANCE"
        
        # 2. Test your code's reaction to that value
        # result = my_app_logic()
        # assert result == "STOP_TRAFFIC"
```

---

## 🔥 Expert: TDD & Integration Testing
Principal engineers follow **TDD (Test-Driven Development)**:
1.  **Red**: Write a test that fails.
2.  **Green**: Write the minimum code to make it pass.
3.  **Refactor**: Clean up the code.

### Integration Tests
Unlike Unit Tests, Integration Tests check if **multiple** components (e.g., Python + Database + Redis) work together correctly. Use **Docker Compose** or **TestContainers** to spawn real infrastructure for these tests.

---

## 🎯 Top 20 Principal Interview Questions (Testing)

1. **Q: What is the difference between a 'Unit Test' and an 'Integration Test'?**
   - **Answer**: A **Unit Test** checks one small piece of code (a function) in total isolation (using Mocks). An **Integration Test** checks if multiple real systems (like your code and a real database) work together.
2. **Q: Why is `pytest` preferred over the built-in `unittest` module?**
   - **Answer**: `pytest` is more "Pythonic." It uses standard `assert` statements instead of verbose `self.assertEqual()`, and its **Fixtures** system is much more powerful and modular.
3. **Q: What is a 'Fixture' in Pytest?**
   - **Answer**: It is a function that provides data or resources (like a DB connection or a config object) to your tests. Fixtures can have different "Scopes" (Function, Module, Session).
4. **Q: Explain 'Mocking' and 'Patching'.**
   - **Answer**: **Mocking** is creating a "Fake" object that behaves like a real one. **Patching** is the process of temporarily replacing a real object in your code with that fake mock object during a test.
5. **Q: What is 'Test Coverage' and is 100% coverage always good?**
   - **Answer**: Coverage is the percentage of your code executed during tests. 100% isn't always proof of quality; it's better to have **High-Quality** tests for critical business logic than empty "check-the-box" tests.
6. **Q: What is the purpose of `pytest.mark.parametrize`?**
   - **Answer**: It allows you to run the **same test** multiple times with different sets of input data, reducing code duplication.
7. **Q: How do you check if a function raises an exception during a test?**
   - **Answer**: Use `with pytest.raises(ValueError):`.
8. **Q: What is the 'Arrange-Act-Assert' pattern?**
   - **Answer**: The industry standard for structuring tests. **Arrange** the data, **Act** (call the function), and **Assert** the result matches expectations.
9. **Q: What is a 'Stub' vs a 'Mock'?**
   - **Answer**: A **Stub** only Provides data (returns a value). A **Mock** can also Record behavior (e.g., "Was this function called twice with these arguments?").
10. **Q: How do you mock an 'Async' function?**
    - **Answer**: Use `unittest.mock.AsyncMock`. It behaves like a normal mock but can be `awaited` inside an async test.
11. **Q: What is the purpose of the `conftest.py` file?**
    - **Answer**: To define **Shared Fixtures** that are available to all test files in a directory and its subdirectories.
12. **Q: Explain 'Monkey Patching' in testing.**
    - **Answer**: Dynamically replacing a method or attribute of a class/module at **Runtime** to facilitate testing.
13. **Q: What is 'TDD' (Test-Driven Development)?**
    - **Answer**: The practice of writing the test **before** writing the code. It forces you to think about the design and the "Contract" of your function first.
14. **Q: How can you skip a test in Pytest?**
    - **Answer**: Use the decorator `@pytest.mark.skip(reason="...")` or `@pytest.mark.skipif(condition)`.
15. **Q: What is 'Snapshot Testing'?**
    - **Answer**: Saving the output of a function (e.g., a large JSON response) and comparing the current output against the saved "Snapshot" to detect changes.
16. **Q: What is the benefit of 'Property-Based' testing (Hypothesis)?**
    - **Answer**: Instead of writing 10 manual inputs, you define the **Properties** of the input (e.g., "Any integer between 1 and 100"), and the library generates hundreds of random cases to find "Edge Case" failures.
17. **Q: What is a 'Regression' test?**
    - **Answer**: A test written to ensure that a bug **stays fixed** after it was found and solved.
18. **Q: How do you test 'Private' methods (starting with `_`)?**
    - **Answer**: Generally, you **don't**. You should test the **Public API** that calls those private methods. If you feel the need to test a private method, it might be a sign it should be moved to a separate class/module.
19. **Q: What is the purpose of `pytest-xdist`?**
    - **Answer**: To run your tests in **Parallel** across multiple CPU cores, which is essential for large test suites that take 10+ minutes to run.
20. **Q: What is the `tmp_path` fixture?**
    - **Answer**: A built-in Pytest fixture that provides a temporary directory unique to that test, which is automatically deleted after the test finishes.

---

[← Previous: AsyncIO](13-asyncio-concurrency.md) | [Next: Level 3 Recap →](../Level-3/15-networking-http.md)
