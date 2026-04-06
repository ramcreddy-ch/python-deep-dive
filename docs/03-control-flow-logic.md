# 03. Control Flow & Logic — Decisions, Loops & Modern Patterns

> "Logic is the 'Brain' of your code. To be an expert, you must move beyond the 'If-Else' ladder and understand how to handle complex data branching with modern patterns like `match/case` and lazy evaluation."

---

## 🌱 The Basics: If-Else & For Loops
At the entry level, we use `if` to make decisions and `for` to repeat actions.

### Basic Syntax
- **if**: "If this is True, do that."
- **elif**: "If the first one wasn't True, check this."
- **else**: "If nothing else worked, do this."

```python
x = 10
if x > 5:
    print("Large")
elif x > 0:
    print("Positive")
else:
    print("Negative")
```

---

## 🌿 Intermediate: Iterating with Range & Enumerate
Senior engineers rarely use `for i in range(len(list))`. We use **Enumerators**.

```python
names = ["Alice", "Bob", "Charlie"]

# Good: (0, Alice), (1, Bob), ...
for i, name in enumerate(names):
    print(f"User {i}: {name}")

# Zip: Joining two lists
ages = [25, 30, 35]
for name, age in zip(names, ages):
    print(f"{name} is {age} years old.")
```

---

## 🌳 Advanced: Comprehensions & Lazy Evaluation
Comprehensions allow for "Functional" logic in a single line. They are often faster than manual loops because they are optimized by the CPython interpreter.

```python
# List Comprehension
squares = [i**2 for i in range(10) if i % 2 == 0]

# Dictionary Comprehension
user_map = {name: age for name, age in zip(names, ages)}
```

---

## 🔥 Expert: Structural Pattern Matching (match/case)
Introduced in Python 3.10, this is the "Secret Weapon" for handling complex data objects (like JSON or API responses).

**Real Use (Platform/MLOps)**:
Handling different incoming event shapes in a single function.

```python
def handle_event(event):
    """
    Expert Pattern: Match/Case. 
    Demonstrates: Complex data branching without 'If-Else' mess.
    """
    match event:
        case {"type": "LOGIN", "user_id": uid}:
            print(f"Logon success for {uid}")
        case {"type": "ERROR", "code": 404, "message": msg}:
            print(f"Page Not Found: {msg}")
        case {"type": "ERROR", "code": code}:
            print(f"Critical System Error: {code}")
        case _:
            print("Unknown Event Shape")
```

---

## 🎯 Top 20 Principal Interview Questions (Control Flow & Logic)

1. **Q: How does the `short-circuit` behavior of `and` / `or` impact performance?**
   - **Answer**: Python only evaluates the second half of a logical expression if necessary. In `A and B`, if `A` is False, `B` is never checked. In `A or B`, if `A` is True, `B` is never checked. Experts use this to put "Expensive" functions (like a DB query) second in a logical chain to avoid running them unless needed.
2. **Q: What is the `loop/else` construct and when should you use it?**
   - **Answer**: A `for` loop can have an `else` block. The `else` block runs **ONLY** if the loop finishes entirely (without hitting a `break`). This is perfect for searching tasks where you want to execute code only if you *don't* find the item.
3. **Q: Explain the difference between `break`, `continue`, and `pass`.**
   - **Answer**: `break` exits the current loop immediately. `continue` skips the rest of the current loop iteration and moves to the next. `pass` is a null operation; it does nothing and is used as a placeholder.
4. **Q: What is the difference between `if x == True` and `if x`?**
   - **Answer**: `if x` checks for **Truthiness** (bool(x) == True). This includes non-empty strings, non-zero numbers, etc. `if x == True` specifically checks if the value is exactly the boolean `True`. Using `if x` is generally considered more Pythonic.
5. **Q: What are 'Truthy' and 'Falsy' values in Python?**
   - **Answer**: **Falsy**: `None`, `False`, `0`, `0.0`, `""`, `[]`, `{}`, `set()`. **Truthy**: Almost everything else.
6. **Q: How does `zip()` handle iterables of unequal length?**
   - **Answer**: It stops at the shortest list. Use `itertools.zip_longest()` if you want to keep going until the longest list finishes.
7. **Q: What is a 'List Comprehension' and why is it faster than a `for` loop?**
   - **Answer**: It's a concise way to create lists. It's faster because the iteration happens in highly-optimized C-code inside the Python interpreter, rather than as separate Python bytecode instructions for each step of a manual loop.
8. **Q: Explain 'Structural Pattern Matching' (match/case) added in 3.10.**
   - **Answer**: It allows for complex data shape checking and variable extraction in one step. It's more powerful than a simple 'Switch' statement because it can match nested dictionaries, lists, and types.
9. **Q: How do you handle a scenario where you need both the index and the value during a loop?**
   - **Answer**: Use `enumerate(my_list)`.
10. **Q: What is the difference between `range(10)` and `list(range(10))`?**
    - **Answer**: `range(10)` is a lazy **Iterator**-like object that only takes a small, constant amount of memory. `list(range(10))` creates a real list of 10 integers in RAM.
11. **Q: Can you use a `while` loop to iterate through a list?**
    - **Answer**: Yes, but `for` is generally preferred unless you need to jump indices or have a condition that isn't just "next item."
12. **Q: What happens if you modify a list while iterating over it?**
    - **Answer**: It can lead to unpredictable behavior (skipping items or infinite loops). The professional way is to iterate over a **copy** of the list (`for x in my_list[:]`) or build a new list using a comprehension.
13. **Q: What is the purpose of `itertools.cycle()`?**
    - **Answer**: To create an infinite iterator that repeats the input collection forever (`A, B, C, A, B, C...`).
14. **Q: How do you exit multiple nested loops at once?**
    - **Answer**: Use a boolean flag, put the loops inside a function and use `return`, or raise a custom exception. Python doesn't have a built-in `break 2`.
15. **Q: What is 'Lazy Evaluation'?**
    - **Answer**: Delaying the calculation of a value until it is actually needed. This is the core strategy of Generators and the `range()` object.
16. **Q: What is the difference between `any()` and `all()`?**
    - **Answer**: `any()` returns True if **at least one** item is Truthy. `all()` returns True only if **every** item is Truthy.
17. **Q: How do you implement a 'Switch' statement in older Python versions (< 3.10)?**
    - **Answer**: Using a **Dictionary Mapping** (keys are conditions, values are functions to call).
18. **Q: What is the 'ternary operator' in Python?**
    - **Answer**: `value_if_true if condition else value_if_false`.
19. **Q: What is the `None` check during a logical chain?**
    - **Answer**: `if my_obj and my_obj.action()` is a safe way to check if an object exists before calling a method on it (short-circuiting).
20. **Q: What is the order of evaluation in `a or b and c`?**
    - **Answer**: `and` has higher precedence than `or`. So it's evaluated as `a or (b and c)`. Always use parentheses for clarity.

---

[← Previous: Data Types](02-data-types-variables.md) | [Next: Functions & Scoping →](04-functions-scoping.md)
