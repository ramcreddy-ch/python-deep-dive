# 04. Functions & Scoping — Reusability, LEGB & Closures

> "Functions are the 'Verbs' of Your Application. To be an expert, you must move beyond simple definitions and understand how Python's 'LEGB' scoping rules and 'Closures' allow for advanced patterns like Decorators and high-performance callbacks."

---

## 🌱 The Basics: Defining a Function
A function is a **Reusable Block of Code**. 
- **Parameter**: The inputs you define (`x`, `y`).
- **Argument**: The actual values you pass (`5`, `10`).
- **Return**: The output your function gives back to the rest of your app.

```python
def add_nums(x, y):
    """Docstring explaining the function's job."""
    return x + y

# Usage
result = add_nums(5, 10)
print(result) # 15
```

---

## 🌿 Intermediate: Positional vs Keyword Arguments
Senior engineers use **Keyword Arguments** for readability and **Default Values** for flexibility.

**The "Clean Code" Rule**:
Always use keyword arguments for anything that isn't immediately obvious.

```python
def send_alert(message, level="INFO", retry=True):
    print(f"[{level}] {message}")

# Good: Readability is high
send_alert(message="Disk Full", level="CRITICAL", retry=False)

# Bad: What is 'False' here?
send_alert("Disk Full", "CRITICAL", False)
```

---

## 🌳 Advanced: *args & **kwargs
What if you don't know how many arguments your function will receive? Use **Packing** and **Unpacking**.

**Real Use (Platform/SRE)**:
A generic logger that takes any number of extra attributes.

```python
def log_event(message, *args, **kwargs):
    # args is a tuple of extra positional inputs
    # kwargs is a dictionary of extra named inputs
    print(f"MESSAGE: {message}")
    for k, v in kwargs.items():
        print(f"DETAIL: {k} = {v}")

# Usage
log_event("Pod Restart", pod_id="worker-99", namespace="prd-1")
```

---

## 🔥 Expert: Scoping Rules (LEGB) & Closures
Python looks for variable names in a specific order: **Local** -> **Enclosing** -> **Global** -> **Built-in**.

### 1. Closures
A closure is a function that "remembers" its environment even after the outer function has finished.

```python
def make_multiplier(n):
    """
    Expert Pattern: Closures. 
    Demonstrates: Returning a custom-tuned function.
    """
    def multiplier(x):
        return x * n # 'n' is "closed over" from the outer scope
    return multiplier

# Create custom functions
times_two = make_multiplier(2)
times_ten = make_multiplier(10)

print(times_two(5)) # 10
print(times_ten(5)) # 50
```

---

## 🎯 Top 20 Principal Interview Questions (Functions & Scoping)

1. **Q: What is the LEGB rule?**
   - **Answer**: The order Python uses to resolve variable names: **L**ocal (inside function), **E**nclosing (outer function), **G**lobal (module level), **B**uilt-in (Python keywords).
2. **Q: Why should you never use a mutable object as a default argument?**
   - **Answer**: Default arguments are evaluated **once** at definition time. If you use a list `def func(items=[])`, every call shares the **same** list object. Use `items=None` instead.
3. **Q: Explain the difference between `*args` and `**kwargs`.**
   - **Answer**: `*args` collects extra positional arguments into a **tuple**. `**kwargs` collects extra keyword arguments into a **dictionary**.
4. **Q: What is a 'Closure' in Python?**
   - **Answer**: A nested function that remembers the environment in its enclosing scope even after the outer function has finished execution.
5. **Q: What is the purpose of the `nonlocal` keyword?**
   - **Answer**: It allows you to modify a variable in the **Enclosing** (outer) scope from within a nested function.
6. **Q: How does the `global` keyword work?**
   - **Answer**: It tells Python to treat a variable name as belonging to the module-level scope, allowing you to modify it from within a function.
7. **Q: What is the difference between a function 'Parameter' and an 'Argument'?**
   - **Answer**: Parameters are the names in the function definition (`x`, `y`). Arguments are the actual values passed during the call (`5`, `10`).
8. **Q: What is a 'Lambda' function and when should you use it?**
   - **Answer**: An anonymous, one-line function. Use it for small, one-time operations like sorting or filtering where a full `def` would be overkill.
9. **Q: What is 'Docstring' and how do you access it via code?**
   - **Answer**: It's a string literal used for documentation inside a function. Access it via `my_func.__doc__` or the `help(my_func)` command.
10. **Q: What is 'Duck Typing' in functions?**
    - **Answer**: Python doesn't check the *type* of an argument; it checks if the argument has the *methods/attributes* needed for the function to work.
11. **Q: Can a Python function return multiple values?**
    - **Answer**: Yes, by returning a **tuple** (e.g., `return a, b`). Python automatically packs them and allows you to unpack them: `val1, val2 = my_func()`.
12. **Q: What is 'Recursion' and what is the default limit?**
    - **Answer**: A function calling itself. The default limit is usually 1,000 calls to prevent stack overflow.
13. **Q: What are 'First-Class Functions'?**
    - **Answer**: It means functions are objects. You can pass them as arguments, return them from other functions, and assign them to variables.
14. **Q: What is the difference between 'Positional' and 'Keyword' arguments?**
    - **Answer**: Positional arguments depend on their order. Keyword arguments are identified by their names (`x=5`), making the order irrelevant.
15. **Q: How do you force a function to accept ONLY keyword arguments?**
    - **Answer**: Use a raw `*` in the parameter list: `def my_func(*, name, age)`. This forces the caller to use names.
16. **Q: What is the `sys.getrecursionlimit()` used for?**
    - **Answer**: To check the maximum depth of the Python interpreter's call stack.
17. **Q: What is 'Memoization'?**
    - **Answer**: An optimization technique where you store the results of expensive function calls and return the cached result when the same inputs occur again (see `functools.lru_cache`).
18. **Q: What is a 'Higher-Order Function'?**
    - **Answer**: A function that either takes another function as an argument (like `map`) or returns a function (like a decorator).
19. **Q: Explain 'Function Annotations' (Type Hints).**
    - **Answer**: Adding types to parameters and returns (`def add(x: int) -> int`). They don't enforce types at runtime but are used by IDEs and static checkers like `mypy`.
20. **Q: What is the `__name__` attribute of a function?**
    - **Answer**: It stores the string name of the function as it was defined in the source code.

---

[← Previous: Control Flow](03-control-flow-logic.md) | [Next: Data Structures →](05-data-structures.md)
