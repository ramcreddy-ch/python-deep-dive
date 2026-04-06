# 02. Data Types & Variables — Mutability, References & Memory

> "In Python, everything is an object. But not all objects are created equal. Understanding the difference between 'What a value is' and 'Where it lives in RAM' is what separates developers from architects."

---

## 🌱 The Basics: What is a Variable?
A variable is a **Name** that points to an **Object**. 

### Basic Types
- **int**: Whole numbers (e.g., `5`, `-10`).
- **float**: Decimals (e.g., `3.14`, `1.0`).
- **str**: Text (e.g., `"Hello"`, `'Python'`).
- **bool**: Logical values (`True`, `False`).

```python
x = 10           # x is a name pointing to an integer object
name = "Python"  # name is a name pointing to a string object
```

---

## 🌿 Intermediate: Mutability
This is a critical concept for preventing bugs in large systems.
- **Immutable**: Once created, they CANNOT be changed. (e.g., `int`, `float`, `str`, `tuple`).
- **Mutable**: They CAN be changed in place. (e.g., `list`, `dict`, `set`).

**The Bug Trap**:
```python
a = [1, 2, 3]
b = a         # b points to the SAME list as a
b.append(4)
print(a)      # a is now [1, 2, 3, 4]!
```

---

## 🌳 Advanced: Memory & References
Python uses "Pass-by-Assignment" (sometimes called pass-by-object-reference). 
- Use `id(x)` to find the memory address of an object.
- Use `is` to check if two names point to the **same** object.
- Use `==` to check if two objects have the **same value**.

**Expert Performance Tip**: 
Python uses **Interning** for small integers (-5 to 256) and short strings. This saves memory by reusing the same objects multiple times.

---

## 🔥 Expert: Object Internals & __slots__
At the principal level, you must understand how Python stores objects in memory.

### 1. The CPython Object Structure
Every Python object has:
1.  **ob_refcnt**: The number of references pointing to it (for the Garbage Collector).
2.  **ob_type**: A pointer to the object's type (to know if it's an int, float, etc.).

### 2. Optimizing with `__slots__`
If you are creating 1,000,000 instances of a class, each one normally has a `__dict__` (a hash table), which is memory-heavy. Using `__slots__` telis Python to use a fixed-size array instead, saving ~50% RAM.

---

## 🎯 Top 20 Principal Interview Questions (Data Types & Variables)

1. **Q: Is everything in Python an object?**
   - **Answer**: Yes. Even basic integers, strings, and functions are objects. This means they all have a memory address (`id()`), a type (`type()`), and a reference count.
2. **Q: What is the difference between `is` and `==`?**
   - **Answer**: `==` checks for **Value Equality** (Do these two objects have the same content?). `is` checks for **Reference Equality** (Do these two names point to the exact same memory address?). 
3. **Q: Why are Strings and Tuples immutable?**
   - **Answer**: For **Safety** (can be used as Hash keys safely) and **Performance** (Interning/caching).
4. **Q: What is CPython's 'Small Integer Caching'?**
   - **Answer**: Python pre-allocates integers from **-5 to 256** when it starts. Every time you use `x = 10`, it points to the same pre-existing object. This avoids the overhead of creating new objects for the most common numbers.
5. **Q: Explain 'Pass-by-Assignment' in Python.**
   - **Answer**: Python passes references to objects, not copies. If the object is mutable (like a list), changes inside a function affect the original. If immutable (like an int), the name is just reassigned locally.
6. **Q: What is the purpose of `__slots__`?**
   - **Answer**: To prevent the creation of `__dict__` for every object instance. This can save **40-50% of RAM** when creating millions of small objects.
7. **Q: What is the difference between a Shallow Copy and a Deep Copy?**
   - **Answer**: **Shallow** copies the top-level container but keeps references to the same inner objects. **Deep** recursively copies every single object, creating a 100% independent clone.
8. **Q: Why can't a `list` be used as a Dictionary key?**
   - **Answer**: Only **Hashable** objects (immutable ones like strings, ints, or tuples of immutable) can be used as keys. A list is mutable, so its content (and thus its hash) could change, breaking the dictionary's lookup logic.
9. **Q: What is 'Interning' in Python?**
   - **Answer**: It is the process of storing only one copy of an object (like a string or small int) and reusing that copy everywhere that value appears.
10. **Q: How does `id(x)` relate to memory?**
    - **Answer**: In CPython, `id(x)` returns the **memory address** of the object in RAM.
11. **Q: What is a 'Circular Reference' and why is it a problem?**
    - **Answer**: When two objects point to each other (A -> B and B -> A). The Reference Counter will never hit 0, potentially causing a memory leak unless handled by the Generational Garbage Collector.
12. **Q: What is the difference between `NULL` in C and `None` in Python?**
    - **Answer**: `NULL` is a pointer to memory address 0. `None` is a **real object** (a singleton) of type `NoneType`.
13. **Q: How do you check the memory size of an object?**
    - **Answer**: Use `sys.getsizeof(obj)`.
14. **Q: What is the difference between `int` and `float` precision?**
    - **Answer**: Python `int` has **Arbitrary Precision** (can grow to any size until RAM is full). `float` follows the IEEE 754 standard (double precision) and can suffer from rounding errors (e.g., `0.1 + 0.2 != 0.3`).
15. **Q: What is a 'Docstring' and how is it stored?**
    - **Answer**: A string literal that appears first in a class/function. It is stored in the `__doc__` attribute of that object.
16. **Q: What is the purpose of `None`?**
    - **Answer**: It represents the absence of a value or a null value. It is a singleton object used as a placeholder.
17. **Q: Can you change the ID of an object?**
    - **Answer**: No. An object's ID is fixed for its entire lifetime.
18. **Q: What is the difference between a bit and a byte in Python memory?**
    - **Answer**: Python handles bits via bitwise operators (`&`, `|`, `^`), but memory is managed in bytes. An empty list takes many bytes (to store its object overhead and array structure).
19. **Q: What is a 'tuple' of one element?**
    - **Answer**: `(1,)`. The comma is required, otherwise `(1)` is just an integer in parentheses.
20. **Q: How do you convert a hex string to an integer?**
    - **Answer**: `int("0xff", 16)`.

---

[← Previous: Getting Started](01-getting-started.md) | [Next: Control Flow & Logic →](03-control-flow-logic.md)
