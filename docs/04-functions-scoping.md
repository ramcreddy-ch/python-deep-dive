# 04. Functions & Scoping — The Building Blocks of Logic

> "A function is more than a container for code; it is a mathematical contract. To reach the expert level, you must understand how Python's 'LEGB' scoping rules search for variables and how Closures allow a function to carry its environment with it like a backpack."

---

## ❓ The 'Why' (High-Level)
Functions are the fundamental unit of abstraction. Without them, software is just a long, unmanageable list of instructions. A principal engineer uses functions to hide detail, create reusable components, and build "Declarative" APIs where the code says **what** to do, but the function handles **how** to do it.

---

## 🌱 Module 1: The Basics (Junior) — The Core Contract
Defining a function is easy; mastering it is a journey.

### 1. Structure of a Function
- **`def`**: The keyword to define a function.
- **Parameters**: The inputs.
- **`return`**: The output.
```python
def greet(name, message="Hello"):
    return f"{message}, {name}!"
```

### 2. Standard Arguments
You can pass arguments by **Position** or by **Keyword**.
```python
greet("Ram", "Hi")         # Positional
greet(message="Hi", name="Ram")  # Keyword (order doesn't matter)
```

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — Flexibility
Mid-level engineers write "Flexible" functions that can handle varying amounts of data.

### 1. `*args` and `**kwargs`
- **`*args`**: Collects extra positional arguments into a **Tuple**.
- **`**kwargs`**: Collects extra keyword arguments into a **Dictionary**.
```python
def build_profile(user_id, *roles, **details):
    print(f"ID: {user_id}, Roles: {roles}, Details: {details}")
```

### 2. Type Hinting & Docstrings
Professional code is self-documenting.
```python
def calculate_tax(amount: float, rate: float = 0.05) -> float:
    """Calculates the total tax for an amount."""
    return amount * rate
```

---

## 🌳 Module 3: Advanced Mechanics (Senior) — Scoping & LEGB
Where does Python look for a variable? It follows the **LEGB Rule**.

1.  **L (Local)**: Inside the current function.
2.  **E (Enclosing)**: Inside a parent function (for nested functions).
3.  **G (Global)**: At the top level of the module.
4.  **B (Built-in)**: Built into the Python language (like `len`).

### The `nonlocal` and `global` Keywords
Use these sparingly. They tell Python to skip the "Local" check and modify a variable in a higher scope.
```python
count = 0
def increment():
    global count
    count += 1
```

---

## 🔥 Module 4: Principal Architect (Principal) — Closures & Frame Objects
A **Closure** is a function that remembers its parent's variables even after the parent has finished running.

### 1. Functional Backpacks
```python
def make_counter(start):
    def count():
        nonlocal start
        start += 1
        return start
    return count

c = make_counter(10)
print(c()) # 11
# The variable 'start' is stored in the 'c.__closure__' attribute!
```

### 2. High-Order Functions
Function names are just pointers. You can pass functions into other functions (like `map`, `filter`) and return them. This is the foundation of **Functional Programming**.

---

## 🏗️ Case Study: The Dynamic Dispatcher
A payment gateway needed to handle 50 different payment methods (Stripe, Paypal, Crypto, etc.).
- **The Junior Approach**: One massive `if/elif` block.
- **The Principal Approach**: A dictionary that maps strings to function names.
- **Result**: To add a new payment method, the team only had to add 1 line to a config file instead of modifying 500 lines of logic.

---

## ⚡ Anti-Patterns & Expert Traps

### 1. The "Mutable Default Argument" Trap (CRITICAL)
**Never** use a list or dictionary as a default argument.
```python
# BAD! The same list is reused every time the function is called.
def add_item(item, basket=[]):
    basket.append(item)
    return basket

# GOOD
def add_item(item, basket=None):
    if basket is None: basket = []
    ...
```

### 2. Overloading Globals
Global variables make it impossible to track state in multi-threaded environments. Always pass data through arguments unless absolutely necessary.

---

## 🎯 Top 20 Principal Interview Questions (Functions & Scoping)

1. **Q: What are the 'LEGB' scoping rules in Python?**
   - **Answer**: It stands for **L**ocal, **E**nclosing, **G**lobal, and **B**uilt-in. This is the order in which Python searches for a variable name when it's accessed in a function.
2. **Q: Why should you avoid using mutable default arguments (like `def f(x=[])`)?**
   - **Answer**: Because the default values are created **only once** at definition time, not every time the function is called. This leads to the "Shared List" bug where multiple calls share and mutate the same object.
3. **Q: What is a 'Closure' in Python?**
   - **Answer**: It is a function object that remembers values in the **enclosing scope** even if they are no longer in memory. It's used to "Pack" variables with a function (accessed via the `__closure__` attribute).
4. **Q: Explain the difference between `global` and `nonlocal`.**
   - **Answer**: `global` tells Python that a variable exists in the **Module-level scope**. `nonlocal` tells Python that a variable exists in the **Next-Higher (Parent) scope**, skip the current local one.
5. **Q: What are `*args` and `**kwargs`?**
   - **Answer**: `*args` is used to pass a variable number of **Positional** arguments (as a tuple). `**kwargs` is used for **Keyword** arguments (as a dictionary).
6. **Q: What is a 'Lambda' function?**
   - **Answer**: It is an **Anonymous** function that can only contain one single expression. It is meant for quick, short-lived logic (e.g., inside a `sort` key).
7. **Q: What are 'First-Class Functions'?**
   - **Answer**: This means functions in Python are treated as **Objects**. They can be assigned to variables, stored in data structures, and passed as arguments to other functions.
8. **Q: Explain 'Positional-Only' (`/`) and 'Keyword-Only' (`*`) parameters.**
   - **Answer**: `/` ensures that all arguments before it MUST be positional. `*` ensures that all arguments after it MUST be keyword-arguments. This is used to build clean and future-proof APIs.
9. **Q: What is the difference between 'Function Definition' and 'Function Invocation'?**
   - **Answer**: **Definition**: Creating the function logic using `def`. **Invocation**: Actually running the function by adding parentheses `()` after its name.
10. **Q: What is the purpose of `functools.wraps`?**
    - **Answer**: When writing decorators, it ensures the metadata (like the function name and docstring) of the original function is preserved and not overwritten by the decorator's wrapper.
11. **Q: What is 'Recursion' and what is the 'Base Case'?**
    - **Answer**: Recursion is a function calling itself. The **Base Case** is the condition that tells the function when to stop calling itself to avoid an infinite loop.
12. **Q: What is 'Shadowing' a variable?**
    - **Answer**: When you create a local variable with the same name as a global or built-in, making it impossible to access the outer one without special syntax.
13. **Q: Explain 'Map', 'Filter', and 'Reduce'.**
    - **Answer**: **Map**: Applies a function to every item in a list. **Filter**: Keeps only items that pass a test. **Reduce**: Combines all items in a list into a single value (e.g., a sum).
14. **Q: What are 'Docstrings' and where are they stored?**
    - **Answer**: Strings written immediately after a function definition to explain its purpose. They are stored in the `__doc__` attribute of the function object.
15. **Q: Can a function in Python return multiple values?**
    - **Answer**: Yes. It's technically returning a **single Tuple** of values, which you can then "Unpack" in the calling code (e.g., `x, y = get_coords()`).
16. **Q: What is 'Late Binding' in Python closures?**
    - **Answer**: The fact that Python only looks up the value of variables in closures **at the time they are called**, not at the time they are created. This can cause issues in loops.
17. **Q: What is a 'Higher-Order Function'?**
    - **Answer**: A function that either **takes a function as an argument** or **returns a function as its result**.
18. **Q: Explain 'Currying' in functional programming.**
    - **Answer**: The technique of transforming a function that takes multiple arguments into a chain of functions that each take a single argument.
19. **Q: What is a 'Decorator'? (Brief intro for Ch 4)**
    - **Answer**: A function that "Wraps" another function to modify its behavior (e.g., adding logging or authentication) without changing its source code.
20. **Q: How can you find all the variables available in the current local scope?**
    - **Answer**: Use the built-in `locals()` function (for current function) or `globals()` (for current module).

---

[Previous: Control Flow](03-control-flow-logic.md) | [Next: Data Structures →](05-data-structures.md)
