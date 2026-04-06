# 03. Control Flow & Logic — Branching, Loops & Bytecode

> "Most bugs are not math errors; they are logic errors. Mastering control flow means writing code that doesn't just work, but is impossible to misread. An expert avoids 'The Pyramid of Doom' and uses Python's modern pattern matching to build clean, declarative systems."

---

## ❓ The 'Why' (High-Level)
Control flow is the "Nervous System" of your application. In a small script, a few `if` statements are fine. In a million-line enterprise system, poorly structured logic leads to **Technical Debt** that can cost millions to fix. A principal engineer knows how to flatten complex logic and when to replace `if/else` chains with **Polymorphism** or **Pattern Matching**.

---

## 🌱 Module 1: The Basics (Junior) — The Core Branching
To start, you need to tell the computer to make decisions.

### 1. The `if`, `elif`, `else` Trinity
These are the standard blocks for decision-making. 
```python
age = 18
if age >= 21:
    print("Full Access")
elif age >= 18:
    print("Partial Access")
else:
    print("No Access")
```

### 2. For and While Loops
- **For**: Used for iterating over a collection (list, string, range).
- **While**: Used for running code until a condition is no longer met.

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — Pythonic Logic
Senior Python code avoids the verbosity of other languages. 

### 1. Ternary Operators & `enumerate()`
Instead of setting a variable inside an `if` block, use the ternary one-liner.
```python
status = "Allow" if authenticated else "Deny"
```
When looping, **never** manually track an index counter. Use `enumerate()`.
```python
for index, name in enumerate(["Ram", "John"]):
    print(f"{index}: {name}")
```

### 2. Structural Pattern Matching (Python 3.10+)
The `match/case` statement is the most powerful addition to Python in a decade. It allows you to "Destructure" data as you check it.
```python
def process_command(cmd):
    match cmd.split():
        case ["quit"]: exit()
        case ["load", filename]: print(f"Loading {filename}")
        case ["move", x, y] if int(x) > 0: print(f"Moving to {x}, {y}")
        case _: print("Unknown command")
```

---

## 🌳 Module 3: Advanced Mechanics (Senior) — The Iterator Protocol
How does a `for` loop actually work? It's not magic; it's a **Protocol**.

### 1. `__iter__` and `__next__`
When you write `for x in my_list:`, Python does this internally:
1.  Calls `iter(my_list)`, which returns an **Iterator** object (calls `__iter__`).
2.  Repeatedly calls `next(iterator)` to get the next item (calls `__next__`).
3.  Catches the `StopIteration` exception to know when to stop.

### 2. Short-Circuiting & Truthiness
In an `if A or B:` statement, if `A` is `True`, Python **skips** evaluating `B` entirely. This "Short-Circuiting" is essential for safety:
```python
if user and user.is_active:  # If user is None, the second part won't run and won't crash.
    ...
```

---

## 🔥 Module 4: Principal Architect (Principal) — Logical Performance
A principal engineer cares about the **Big-O complexity** of their logic.

### 1. The Cost of Membership (`in`)
- **List**: `x in my_list` is **O(n)** (slow as the list grows).
- **Set/Dict**: `x in my_set` is **O(1)** (instant, regardless of size).
*Always convert lists to sets if you are doing frequent membership checks.*

### 2. Bytecode Analysis
Python's compiler optimizes simple loops.
```python
import dis
def loop_test():
    for i in range(10): pass
dis.dis(loop_test)
# Look for FOR_ITER and JUMP_ABSOLUTE. Experts use this to see if their 
# 'Clever' logic is actually generating more work for the interpreter.
```

---

## 🏗️ Case Study: Flattening the 'Pyramid of Doom'
A major e-commerce gateway had a validation function with **7 nested if-statements** to check order integrity. It was impossible to test.
- **The Solution**: The team refactored it using **Guard Clauses**. Instead of wrapping the "Success" code in deep layers, they "Returned Early" for every failure.
- **Result**: The code became linear, readable, and the number of production bugs dropped by 50% in that module.

---

## ⚡ Anti-Patterns & Expert Traps
- **Trap 1: Mutating a list while iterating over it**: This causes skipped items or crashes. **Expert fix**: Iterate over a copy `for x in my_list[:]` or use a list comprehension to build a new list.
- **Trap 2: Using `== True` or `== False`**: In Python, just use `if condition:` or `if not condition:`.
- **Trap 3: Deep Nesting**: If you are more than 3 levels deep, **Refactor** into a separate function.

---

## 🎯 Top 20 Principal Interview Questions (Control Flow & Logic)

1. **Q: What is the difference between `range()` in Python 2 and Python 3?**
   - **Answer**: In Python 2, `range()` created a physical **List** in memory. In Python 3, `range()` is a **Generator-like object** (an immutable sequence) that calculates numbers on-the-fly, saving massive amounts of memory.
2. **Q: Explain 'Short-circuit Evaluation' in Python.**
   - **Answer**: In logical expressions (`and`/`or`), Python stops evaluation as soon as the outcome is determined. For `A or B`, if `A` is True, `B` is not evaluated. This is often used to prevent `AttributeError` (e.g., `if obj is not None and obj.value > 0`).
3. **Q: What is a 'Truthiness'?**
   - **Answer**: The concept that non-boolean objects can be evaluated in an `if` statement. Objects like `0`, `""`, `[]`, `{}`, `None`, and `set()` are **Falsy**. Almost everything else is **Truthy**.
4. **Q: How does a `for` loop work internally? (The Iterator Protocol)**
   - **Answer**: It calls `iter()` on the object to get an iterator, then repeatedly calls `next()` on that iterator until a `StopIteration` exception is raised.
5. **Q: What is the difference between `break` and `continue`?**
   - **Answer**: `break` exits the entire loop immediately. `continue` skips the rest of the current iteration and jumps to the next one.
6. **Q: What is the purpose of the `else` clause in a `for` or `while` loop?**
   - **Answer**: The `else` block runs **only if the loop finished naturally** (i.e., it was NOT terminated by a `break` statement). It's useful for "search" loops.
7. **Q: What is 'Structural Pattern Matching' (Match-Case) and when was it introduced?**
   - **Answer**: Introduced in Python 3.10. It allows for complex branching based on the **Shape and Content** of data, rather than just simple value comparisons. It supports destructuring of lists and dictionaries.
8. **Q: Explain the `any()` and `all()` functions.**
   - **Answer**: `any()` returns True if **at least one** element in an iterable is truthy. `all()` returns True only if **every** element is truthy. Both are short-circuiting.
9. **Q: Why is `while 1` sometimes considered faster than `while True` in older Python versions?**
   - **Answer**: In Python 2, `True` was a global variable that could be reassigned, requiring a lookup. `1` was a constant. In Python 3, this is no longer an issue as `True` is a keyword.
10. **Q: What is the complexity of searching for an item in a `List` vs a `Set`?**
    - **Answer**: List: **O(n)** (linear search). Set: **O(1)** (hash table lookup). Always use sets for high-frequency membership tests.
11. **Q: What is 'The Pyramid of Doom' and how do you fix it?**
    - **Answer**: Code that is deeply nested with `if` statements. Fix it using **Guard Clauses** (returning early on failure) to keep the "Happy Path" at the lowest level of indentation.
12. **Q: Can you use a `return` statement inside a loop?**
    - **Answer**: Yes. It will immediately terminate the loop **and** the function, returning the value to the caller.
13. **Q: What is the difference between `if x:` and `if x is True:`?**
    - **Answer**: `if x:` checks for **Truthiness** (e.g., a non-empty list would pass). `if x is True:` checks if `x` is literally the boolean object `True`. The former is almost always preferred.
14. **Q: How do you iterate over two lists simultaneously?**
    - **Answer**: Use the `zip()` function: `for a, b in zip(list1, list2):`. For different lengths, use `itertools.zip_longest()`.
15. **Q: What is the `pass` statement used for?**
    - **Answer**: It is a **Null Operation**. It acts as a placeholder when a statement is syntactically required but you don't want to execute any code (e.g., in an empty class or function).
16. **Q: Explain the 'Walrus Operator' (`:=`) and its impact on control flow.**
    - **Answer**: introduced in 3.8, it allows you to **assign a variable within an expression**. This is useful in `while` loops or `if` statements to avoid redundant function calls.
17. **Q: What is a 'Nested Comprehension'?**
    - **Answer**: A list/dict comprehension that contains another comprehension. While powerful, they should be used sparingly as they can quickly become unreadable.
18. **Q: How does Python handle recursion limits?**
    - **Answer**: Python has a maximum recursion depth (usually 1,000) to prevent stack overflows. You can check it with `sys.getrecursionlimit()` and change it with `sys.setrecursionlimit()`, though refactoring to a loop is usually better.
19. **Q: What is the `itertools` module?**
    - **Answer**: A standard library module providing high-performance, memory-efficient tools for complex iteration (e.g., `chain`, `cycle`, `product`).
20. **Q: What is the difference between a 'Statement' and an 'Expression'?**
    - **Answer**: An **Expression** evaluates to a value (e.g., `2 + 2`). A **Statement** is an instruction that performs an action (e.g., `x = 4` or `if x: ...`). In Python 3, many former statements (like `print`) became functions (expressions).

---

[Previous: Data Types](02-data-types-variables.md) | [Next: Functions →](04-functions-scoping.md)
