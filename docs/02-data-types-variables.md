# 02. Data Types & Internals — Memory, Objects & Immutability

> "In Python, everything is an object. To move from junior to expert, you must understand that even a simple '1' carries a 28-byte overhead and a pointer to a type structure. Mastering data types is about understanding the memory they consume and the cost of the operations you perform on them."

---

## ❓ The 'Why' (High-Level)
In low-level languages like C, an `int` is just 4 or 8 bytes of raw memory. In Python, an `int` is a **Full Object** (`PyObject`). This abstraction allows Python to be flexible and secure, but at the cost of performance and RAM. A principal engineer knows when to use a standard list and when to bypass Python's object overhead using tools like `NumPy` or `array`.

---

## 🌱 Module 1: The Basics (Junior) — The Core Types
Python has four primary "Primitive" types that you'll use 90% of the time.

### 1. Integers & Floats
- **Int**: Whole numbers. Python 3's integers have **arbitrary precision**, meaning they can be as large as your RAM allows.
- **Float**: Decimal numbers. These follow the **IEEE 754** double-precision standard.

### 2. Strings & Booleans
- **Str**: A sequence of Unicode characters.
- **Bool**: `True` or `False`. (Note: `True` is represented as `1` and `False` as `0` internally).

### 3. The Concept of Immutability
This is the most critical lesson for beginners. 
- **Immutable**: Once created, it cannot be changed (Int, Float, String, Tuple).
- **Mutable**: It can be modified in place (List, Dict, Set).
```python
s = "Hello"
s[0] = "J"  # ERROR! Strings are immutable.
```

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — Collections
To more from basic to mid-level, you must master how to store and manipulate groups of data.

### 1. Lists vs. Tuples
- **List `[]`**: Mutable. Best for data that changes.
- **Tuple `()`**: Immutable. Faster and consumes less memory. Use it for data that shouldn't change (like a coordinate `(x, y)`).

### 2. Dictionaries & Sets
- **Dict `{}`**: Key-Value pairs. Extremely fast lookup (O(1)).
- **Set `{}`**: Unique values only. Perfect for removing duplicates from a list.

### 3. Type Hinting
Professional code uses type hints to make it readable and catch bugs before they happen.
```python
def process_user(user_id: int, name: str) -> bool:
    return True
```

---

## 🌳 Module 3: Advanced Mechanics (Senior) — The C-Level
What is an object? In the CPython source code, every object starts with a structure called `PyObject`.

### 1. The `PyObject` Structure
Every object in your memory contains:
1.  **ob_refcnt**: Reference Count (for the Garbage Collector).
2.  **ob_type**: A pointer to the object's **Type** (so Python knows it's an `int` or a `list`).
3.  **ob_size**: (For variable-sized objects like lists and strings).

### 2. Arbitrary Precision Internals
How does Python handle a 100-digit number? It stores the integer as an array of "digits" (usually 30-bit pieces). When you do `a + b`, it performs "schoolbook addition" across these pieces. It's slower than hardware math but infinitely flexible.

---

## 🔥 Module 4: Principal Architect (Principal) — Memory Optimization
A principal engineer cares about the **RAM footprint** of the system.

### 1. Integer Caching (The "Interning" Trap)
Python pre-allocates integers from **-5 to 256** at startup.
```python
a = 256
b = 256
print(a is b)  # True (They point to the EXACT same memory address)

x = 257
y = 257
print(x is y)  # False (They are different objects with the same value)
```

### 2. Floating Point Precision Pitfalls
Never use `float` for currency! Because it uses binary fractions, `0.1 + 0.2` will equal `0.30000000000000004`. 
- **The Expert Solution**: Use the `decimal` module for financial calculations.

---

## 🏗️ Case Study: Memory Optimization at Scale
A large financial platform was processing millions of transactions per second. Using standard Python dictionaries to store transaction data was consuming 40GB of RAM per server.
- **The Optimization**: By switching to **`__slots__`** in their classes and using **`namedtuples`** for data storage, they reduced memory usage by 70%, allowing the service to run on much smaller, cheaper cloud instances.

---

## ⚡ Anti-Patterns & Expert Traps
- **Trap 1: String Concatenation in Loops**: Doing `s += new_str` in a loop creates a *new string* every time, slowing down exponentially. **Expert fix**: Collect parts in a list and use `"".join(parts)`.
- **Trap 2: Mutable Default Arguments**: (Covered in Ch 4, but critical).
- **Trap 3: Using `is` for value comparison**: Always use `==` for values. Use `is` only for identity (e.g., `is None`).

---

## 🎯 Top 20 Principal Interview Questions (Data Types & Internals)

1. **Q: Why are strings immutable in Python?**
   - **Answer**: For consistency and performance. Immutability allows strings to be used as **Dictionary Keys** (because their hash value won't change) and allows for **String Interning** to save memory.
2. **Q: Explain the difference between `is` and `==`.**
   - **Answer**: `is` checks for **Identity** (do both point to the same physical memory address?). `==` checks for **Equality** (do they have the same value?).
3. **Q: What is 'Duck Typing'?**
   - **Answer**: A style of programming where the type of an object is determined by its **Methods and Properties**, not by its explicit class. "If it walks like a duck and quacks like a duck, it is a duck."
4. **Q: How does Python handle integers larger than 64 bits?**
   - **Answer**: Using **Arbitrary Precision Arithmetic**. Python stores large integers as an array of 'digits' and performs operations on them in software, ensuring no overflow occurs as long as RAM is available.
5. **Q: What is 'String Interning'?**
   - **Answer**: An optimization where Python stores only **one copy** of certain strings in a global "intern pool." This makes comparisons much faster (pointer comparison instead of char-by-char).
6. **Q: Why should you never use `float` for financial data?**
   - **Answer**: Floats use **Binary Fractional Representation** (IEEE 754), which cannot precisely represent many decimal numbers (like 0.1). This leads to rounding errors. Use `decimal.Decimal` instead.
7. **Q: What is a `PyObject` in CPython?**
   - **Answer**: The base structure for all Python objects in the C source code. It contains a **Reference Count** and a **Pointer to the Type Structure**.
8. **Q: Explain the 'Small Integer Caching' optimization.**
   - **Answer**: Python pre-allocates and reuses integer objects in the range **-5 to 256**. Any variable pointing to an integer in this range will point to the same memory address.
9. **Q: What is the difference between a `List` and an `Array` (from the `array` module)?**
   - **Answer**: A **List** can hold objects of any type (it's an array of pointers). The **`array`** module stores primitive types (like ints or floats) contiguously in memory, which is much more RAM-efficient for millions of items.
10. **Q: What is a 'Hashable' object?**
    - **Answer**: An object that has a hash value which never changes during its lifetime (requires `__hash__`). All immutable built-in types (str, int, tuple) are hashable; mutable ones (list, dict) are not.
11. **Q: Explain 'Deep Copy' vs 'Shallow Copy'.**
    - **Answer**: A **Shallow Copy** creates a new object but points to the *existing* children. A **Deep Copy** creates a new object and recursively creates new copies of ALL its children.
12. **Q: What is the purpose of `__slots__`?**
    - **Answer**: It tells Python not to use a dynamic dictionary (`__dict__`) for an object's attributes, instead using a fixed-size array. This significantly reduces memory usage for classes with many instances.
13. **Q: Why are Lists slower than Tuples for certain operations?**
    - **Answer**: Lists are **Over-allocated** (they keep extra empty slots to make appending fast) and they are mutable, which requires more internal bookkeeping. Tuples are fixed-size and immutable.
14. **Q: What is a `bytearray`?**
    - **Answer**: A mutable version of the `bytes` object. It's useful for high-performance binary data manipulation (like editing image data or network packets in place).
15. **Q: How does Python's `bool` type relate to `int`?**
    - **Answer**: `bool` is a **Subclass of `int`**. `True` is 1 and `False` is 0. This is why you can technically do `True + True` and get `2`.
16. **Q: What is the complexity of a Dictionary lookup?**
    - **Answer**: Average case **O(1)**. In the worst case (many hash collisions), it can be O(n).
17. **Q: What is 'Object Pool' or 'Freelist' in CPython?**
    - **Answer**: An internal mechanism where CPython reuses the memory of recently deleted small objects (like small lists or dicts) to avoid expensive calls to the system's `malloc`.
18. **Q: Explain the difference between `str` and `bytes` in Python 3.**
    - **Answer**: `str` represents **Human-readable text** (Unicode). `bytes` represents **Raw binary data**. You must "Encode" a string into bytes and "Decode" bytes into a string.
19. **Q: What is the purpose of the `collections.deque`?**
    - **Answer**: A **Double-Ended Queue**. Unlike a list, it allows for O(1) additions and removals from **both** the beginning and the end.
20. **Q: How do you check the memory size of an object in Python?**
    - **Answer**: Use `sys.getsizeof(obj)`. Keep in mind it only returns the size of the container, not the objects it contains.

---

[Previous: Getting Started](01-getting-started.md) | [Next: Control Flow →](03-control-flow-logic.md)
