# 05. Data Structures & Collections — Dicts, Sets & Internals

> "Choosing the wrong data structure is the #1 cause of performance death in Python. An expert needs to know not just how to use a dictionary, but why it's O(1) and when a `defaultdict` or `namedtuple` is the professional choice."

---

## 🌱 The Basics: Lists, Tuples & Sets
At the entry level, we store collections of data.

- **List `[]`**: Ordered, mutable collection. Best for sequences of items of the same type.
- **Tuple `()`**: Ordered, **immutable** collection. Faster than lists and safer for fixed data (like GPS coordinates).
- **Set `{}`**: Unordered, unique items. Best for membership checking (`x in my_set`) and removing duplicates.

```python
names = ["Alice", "Bob"] # List
point = (10, 20)         # Tuple
unique_ids = {101, 102}  # Set
```

---

## 🌿 Intermediate: Dictionaries (Key-Value)
The dictionary (`dict`) is the most important data structure in Python. It maps a **Unique Key** to a **Value**.

```python
# Basic Dict
user = {"id": 1, "name": "Alice"}
print(user["name"]) # "Alice"

# Safe access with .get()
# This avoids 'KeyError' if the key is missing
role = user.get("role", "GUEST")
```

---

## 🌳 Advanced: Specialized Collections
Python's `collections` module provides "Experts-Only" tools for complex engineering.

### 1. `defaultdict` vs `OrderedDict` vs `Counter`
- **defaultdict**: Automatically creates a default value if a key is missing. Perfect for grouping items.
- **OrderedDict**: Remembers the order in which items were inserted (Note: Standard `dict` also does this since 3.7, but `OrderedDict` has better reordering methods).
- **Counter**: High-speed frequency counting.

```python
from collections import defaultdict, Counter

# Expert Pattern: Grouping with defaultdict
groups = defaultdict(list)
groups["SRE"].append("Alice")
groups["SRE"].append("Bob") 
# No need to check if "SRE" exists first!

# Frequency counting
word_freq = Counter(["apple", "banana", "apple"])
print(word_freq["apple"]) # 2
```

---

## 🔥 Expert: Dict Internals & Hash Tables
At the principal level, you must understand **How** it works to optimize it.

### 1. The Hash Table Logic
Dictionaries are implemented as **Hash Tables**.
1.  Python takes your key and runs a `hash()` function on it.
2.  The resulting number is used as an index in an underlying array.
3.  **Performance**: This makes looking up a key **O(1)** (constant time), regardless of whether you have 10 keys or 10,000,000.

### 2. Space-Time Trade-off
Dictionaries use a lot of memory to maintain that speed. If you have 100M attributes, consider using **NamedTuples** or **DataClasses** with `__slots__` to save RAM.

---

## 🎯 Top 20 Principal Interview Questions (Data Structures)

1. **Q: How does a `dict` maintain O(1) lookup time?**
   - **Answer**: It uses a **Hash Table**. The key's hash value is mapped to an index in an internal array, allowing for near-instant retrieval regardless of content size.
2. **Q: What is a 'Hash Collision' and how does Python handle it?**
   - **Answer**: This occurs when two different keys produce the same hash index. Python handles this using **Open Addressing** (finding the next available "slot" in the array).
3. **Q: What is the difference between a `list` and a `tuple` in memory?**
   - **Answer**: A **list** is mutable and 'Over-allocated' to allow for fast appends. A **tuple** is immutable, has a fixed size, and is generally more memory-efficient as it doesn't need extra 'empty' slots.
4. **Q: When would you use a `set` over a `list`?**
   - **Answer**: Use a **set** when you need unique items and fast membership checking (`if x in my_set`). In a set, this is **O(1)**; in a list, it is **O(n)**.
5. **Q: What is the purpose of `collections.defaultdict`?**
   - **Answer**: It automatically creates a default value (like an empty list or integer 0) when you access a key that doesn't exist, preventing a `KeyError`.
6. **Q: What is a `namedtuple`?**
   - **Answer**: A memory-efficient subclass of a tuple where you can access fields by **Name** (`user.id`) instead of just index (`user[0]`). It's a "Lightweight Class."
7. **Q: Explain the difference between `list.sort()` and `sorted(list)`.**
   - **Answer**: `list.sort()` sorts the list **in place** and returns `None`. `sorted(list)` returns a **new** sorted list, leaving the original unchanged.
8. **Q: How can you reverse a list in-place?**
   - **Answer**: Use `my_list.reverse()`. To create a *new* reversed list, use `my_list[::-1]`.
9. **Q: What is the time complexity of removing an item from the *middle* of a list?**
   - **Answer**: **O(n)**. Python must 'Shift' all subsequent items to close the gap.
10. **Q: What is `collections.deque` and when to use it?**
    - **Answer**: A "Double-Ended Queue." Use it when you need to add/remove items from **Both Ends** of a collection with **O(1)** performance. Standard lists are slow (O(n)) for removing from the front.
11. **Q: Why can't a `set` contain a `list`?**
    - **Answer**: Because a list is **Mutable** and therefore not **Hashable**. A set requires all its items to have a stable hash value that never changes.
12. **Q: What is the difference between `dict.keys()` and `list(dict.keys())`?**
    - **Answer**: `dict.keys()` returns a **View Object** that reflects any changes made to the dictionary in real-time. `list(dict.keys())` creates a static 'Snapshot' of the keys at that moment.
13. **Q: How do you merge two dictionaries in Python 3.9+?**
    - **Answer**: Use the merge operator `dict1 | dict2`. In older versions, use `{**dict1, **dict2}`.
14. **Q: What is 'Dictionary Comprehension'?**
    - **Answer**: A concise way to build dictionaries: `{key: val for key, val in iterable}`. It's faster than a manual loop.
15. **Q: What is the `sys.getsizeof()` for an empty list vs an empty dict?**
    - **Answer**: An empty dict is significantly larger than an empty list because the dict must pre-allocate space for its hash table structure.
16. **Q: What is `collections.Counter`?**
    - **Answer**: A specialized dict for counting the frequency of hashable items in an iterable.
17. **Q: How does `list.extend()` differ from `list.append()`?**
    - **Answer**: `append()` adds one single object to the end. `extend()` takes an iterable (like another list) and adds **each item** from it to the end.
18. **Q: What is the 'Slicing' operator `[start:stop:step]`?**
    - **Answer**: A powerful way to extract parts of a list, string, or tuple. `[::-1]` is the common idiom for reversing a collection.
19. **Q: What is a 'Frozenset'?**
    - **Answer**: An **Immutable** version of a set. Because it's immutable, it is **Hashable** and can be used as a Dictionary key or added to another Set.
20. **Q: What is the difference between `dict` insertion order in Python 3.6 vs 3.7+?**
    - **Answer**: Since 3.7, dictionaries are **guaranteed** to remember insertion order. In 3.6, it was an implementation detail of CPython but not official in the language spec.

---

[← Previous: Functions](04-functions-scoping.md) | [Next: Error Handling →](06-error-handling.md)
