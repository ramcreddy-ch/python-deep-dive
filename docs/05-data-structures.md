# 05. Data Structures — Lists, Dicts & Hash Table Internals

> "Choosing the wrong data structure is the #1 cause of performance death in Python. An expert needs to know not just how to use a dictionary, but why it's O(1) and how Python handles hash collisions under the hood to ensure scaling at millions of operations per second."

---

## ❓ The 'Why' (High-Level)
In Python, data structures are the "Containers" for your logic. While it's easy to just use a `list` for everything, doing so can turn a fast application into a slow one as data grows. A principal engineer chooses a structure based on **Time Complexity** (O-notation) and **Memory Footprint**. 

---

## 🌱 Module 1: The Basics (Junior) — The Core Four
Python provides four built-in collection types that handle 95% of use cases.

### 1. Lists `[]` & Tuples `()`
- **List**: An ordered, mutable collection. Use it when you need to store items in a specific order and change them later.
- **Tuple**: An ordered, **immutable** collection. It's faster and safer for data that shouldn't change (like fixed coordinates or database records).

### 2. Dictionaries `{}` & Sets `{}`
- **Dict**: A mapping of unique Keys to Values.
- **Set**: A collection of **unique** items only.
```python
fruits = ["apple", "apple", "orange"]
unique_fruits = set(fruits)  # Result: {"apple", "orange"}
```

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — Efficient Usage
Junior engineers use these structures; mid-level engineers use them **efficiently**.

### 1. Lists as Stacks and Queues
- **Stack (LIFO)**: Use `append()` and `pop()`.
- **Queue (FIFO)**: Use `collections.deque` (it allows for O(1) removals from the beginning, unlike a standard list).

### 2. Dictionary Power-Methods
Avoid `KeyError` using `get()` and `setdefault()`.
```python
counts = {}
# The 'Professional' way to increment a count
counts["apple"] = counts.get("apple", 0) + 1
```

---

## 🌳 Module 3: Advanced Mechanics (Senior) — Hash Tables
A **Dictionary** is actually a **Hash Table**. This is why lookups are so fast (O(1)).

### 1. The Hashing Process
When you store a key `x` in a dictionary:
1.  Python calls `hash(x)` to get an integer.
2.  It uses that integer to find a specific "Bucket" in memory.
3.  If two keys have the same hash (**Collision**), Python uses **Open Addressing** (scanning for the next empty slot) to store the data.

### 2. List Over-Allocation
When a list is full and you `append()` another item, Python doesn't just add one slot. It creates a **New, larger array** (usually with 12.5% to 50% extra space) and copies the old items over. This ensures most appends are very fast (O(1) "Amortized").

---

## 🔥 Module 4: Principal Architect (Principal) — Performance Optimization
At the highest level, you optimize for **Memory and Throughput**.

### 1. The `collections` Module
- **`defaultdict`**: Automatically creates a default value for a missing key.
- **`Counter`**: A high-speed dictionary for counting objects.
- **`OrderedDict`**: (Prior to Python 3.7) Guaranteed order. (Now standard in 3.7+).

### 2. Sorted Collections with `bisect`
If you have a massive sorted list and want to keep it sorted after an insert, don't just `.sort()` again (O(n log n)). Use the **`bisect`** module to find the insertion point in **O(log n)** time.

---

## 🏗️ Case Study: The High-Frequency Tracker
A monitoring service was tracking 1,000,000 unique IP addresses. Using a `list` to check if an IP was already seen caused the CPU to hit 100% due to the O(n) search time.
- **The Solution**: By simply converting the IP list to a **`set`**, the lookup time dropped from **seconds** to **microseconds** (O(1)). 
- **Result**: The server load dropped from 100% to 5%, allowing the team to decommission 10 out of 12 servers.

---

## ⚡ Anti-Patterns & Expert Traps

### 1. Using a List for Membership Tests
`if item in my_list:` is slow. As the list grows to 10k items, this statement becomes 10,000 times slower. **Expert fix**: If you are checking existence frequently, use a `set`.

### 2. Deep-Copying massive structures
`copy.deepcopy(massive_dict)` is extremely slow and memory-intensive. Most engineers only need a "Shallow Copy" `massive_dict.copy()`.

---

## 🎯 Top 20 Principal Interview Questions (Data Structures)

1. **Q: How does a Python Dictionary achieve O(1) lookup time?**
   - **Answer**: By using a **Hash Table**. It converts the key into a hash value, which identifies a direct memory address (bucket) for the data, avoiding the need to scan through the collection.
2. **Q: What is a 'Hash Collision' and how does Python resolve it?**
   - **Answer**: It's when two different keys generate the same hash index. Python uses **Open Addressing** (specifically pseudo-random probing) to search for the next available slot in the table.
3. **Q: Why are Lists mutable but Tuples are not?**
   - **Answer**: Lists are designed to be dynamic containers for unknown data counts. Tuples are designed to be "Fixed Records" or structures whose identity and content are safe from accidental change.
4. **Q: What is the complexity of inserting an item at the beginning of a `List`?**
   - **Answer**: **O(n)**. Every existing item in the list must be shifted forward by one position in memory.
5. **Q: When would you use a `collections.deque` over a `List`?**
   - **Answer**: When you need to frequently add or remove items from **both ends** of a collection (e.g., in a Queue). Deque permits this in O(1), whereas removing from the front of a list is O(n).
6. **Q: What is a 'Hashable' object? Can a list be a dictionary key?**
   - **Answer**: A hashable object is one whose hash value never changes (requires `__hash__`). No, a **List cannot be a dictionary key** because it is mutable and its hash could change, making it "unfindable" in the hash table.
7. **Q: Explain 'Amortized O(1) Time Complexity' in the context of `list.append()`.**
   - **Answer**: While most appends are O(1), occasionally a list must be **Resized** (which is O(n)). However, because the resize happens so infrequently, the "Average" cost per append remains O(1).
8. **Q: What is the purpose of the `collections.Counter`?**
   - **Answer**: A subclass of `dict` designed specifically for counting hashable objects. It's much faster and cleaner than manually building a count dictionary.
9. **Q: What is the `bisect` module used for?**
   - **Answer**: To maintain a **Sorted List** without having to sort it again after every insertion. It uses **Binary Search** to find the correct insertion index in O(log n) time.
10. **Q: How can you remove duplicates from a list while maintaining its order?**
    - **Answer**: Use `dict.fromkeys(my_list).keys()`. This preserves the order because Python 3.7+ dictionaries are ordered by default.
11. **Q: What is the difference between `list.sort()` and `sorted(list)`?**
    - **Answer**: `list.sort()` modifies the original list **in-place** (returning None). `sorted(list)` creates a **New sorted list** and leaves the original one unchanged.
12. **Q: Explain 'Dictionary View Objects' (`keys()`, `values()`, `items()`).**
    - **Answer**: These are dynamic views that stay updated. If the dictionary changes, the view reflects the change instantly without creating a separate list copy.
13. **Q: What is the maximum size of a Python List?**
    - **Answer**: It is limited only by your available **RAM** and the address space of your OS.
14. **Q: What is a `defaultdict`?**
    - **Answer**: A dictionary that provides a default value (e.g., an empty list `[]` or the integer `0`) if a key is missing, avoiding the need for `if key in dict` checks.
15. **Q: Explain 'Slicing' in lists and its performance impact.**
    - **Answer**: Slicing (`list[a:b]`) creates a **New list object** and copies the references to the items. It is an O(k) operation where k is the length of the slice.
16. **Q: What is the purpose of `frozenset`?**
    - **Answer**: It is an **Immutable Set**. Because it cannot be changed, it is **Hashable**, meaning a frozenset can be used as a Dictionary Key (unlike a standard set).
17. **Q: How does the size of a dictionary change when you remove items?**
   - **Answer**: Surprisingly, in CPython, a dictionary **does not shrink** in memory when items are removed. To shrink it, you must create a new dictionary or wait for it to be completely re-indexed during a mass insert.
18. **Q: What is the `__contains__` method?**
    - **Answer**: It is the method called when you use the `in` operator. Implementing it in a custom class allows you to define custom logic for membership tests.
19. **Q: What is 'Tuple Unpacking'?**
    - **Answer**: The ability to extract values from a tuple directly into variables: `x, y = (10, 20)`. This also works for lists and sets.
20. **Q: Why did Python 3.7 make Dictionaries ordered?**
    - **Answer**: It was a side-effect of a new, more memory-efficient hash table implementation. It became a language guarantee in 3.7+ because it made many programming patterns cleaner.

---

[Previous: Functions](04-functions-scoping.md) | [Next: Error Handling →](06-error-handling.md)
