# 08. Object-Oriented Programming — Classes, Inheritance & Composition

> "A class isn't just a container for data. To be an expert, you must understand that OOP is about 'Encapsulation' and 'Polymorphism' — building blueprints that allow your system to grow without collapsing under the weight of its own complexity."

---

## ❓ The 'Why' (High-Level)
In any large-scale application (like a banking system or a social network), procedural "spaghetti code" becomes impossible to maintain. **Object-Oriented Programming (OOP)** allows you to group data and behavior into logical "Objects" that represent real-world entities. A principal engineer uses OOP to build **Modular** and **Swappable** components, ensuring that changing how a "User" is saved doesn't break the entire "Order" processing system.

---

## 🌱 Module 1: The Basics (Junior) — The Core Blueprint
A **Class** is the factory; an **Object** is the product.

### 1. The `__init__` constructor & `self`
`self` is a reference to the **specific instance** being created.
```python
class User:
    def __init__(self, username):
        self.username = username  # Instance attribute

me = User("ramcreddy")
```

### 2. Methods vs Functions
A **Method** is just a function that "belongs" to an object and can access its data via `self`.

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — The 3 Pillars

### 1. Inheritance (Code Reuse)
Why rewrite code? If a `Staff` user is just a `User` with extra powers, inherit from it.
```python
class Staff(User):
    def delete_post(self): pass
```

### 2. Encapsulation (Privacy)
Python uses single-underscore `_` to signal that an attribute is "Internal" and shouldn't be touched by outside code. Double-underscore `__` triggers **Name Mangling** to make it truly private.

### 3. @property (The Getter/Setter)
Avoid public attributes if you need to validate them later. Use `@property` to turn a method into an attribute.
```python
class Account:
    @property
    def balance(self): return self._balance
```

---

## 🌳 Module 3: Advanced Mechanics (Senior) — MRO & super()
Senior engineers understand the "Diamond Problem" of multiple inheritance.

### 1. Method Resolution Order (MRO)
If a class inherits from A and B, and both have a `save()` method, which one is called? Python uses the **C3 Linearization algorithm** to decide.
- **Inspect it**: `MyClass.__mro__` shows the exact search path.

### 2. The `super()` Power
`super()` doesn't just call the "Parent." It calls the **next class in the MRO**. This is essential for clean, cooperative multiple inheritance.

---

## 🔥 Module 4: Principal Architect (Principal) — Memory & Creation
At the highest level, you optimize how objects are born and stored.

### 1. `__slots__` for Massive Scaling
By default, every Python object has a dynamic dictionary (`__dict__`) to store attributes. If you have 10,000,000 objects, this is a massive memory waste.
- **Solution**: Use `__slots__` to store attributes in a fixed-size array instead.
```python
class Point:
    __slots__ = ("x", "y") # No __dict__! Saves 60-80% RAM!
```

### 2. `__new__` vs `__init__`
- **`__new__`**: Creates the object in memory (The "Factory").
- **`__init__`**: Fills the object with data (The "Painter").
- **Principal Use**: Overriding `__new__` to implement the **Singleton** pattern (always returning the same object).

---

## 🏗️ Case Study: The Multi-Vendor Payment Gateway
A platform needed to support PayPal, Stripe, and Adyen.
- **The Junior Approach**: Three different classes with different method names like `pay_paypal()` and `make_stripe_payment()`. (Hard to maintain).
- **The Principal Approach**: Used an **Abstract Base Class (ABC)** to enforce a universal `process_payment()` interface across all vendors.
- **Result**: The core checkout system didn't care which vendor was used—it just called `vendor.process_payment()`, allowing the business to add a 4th vendor in mere hours.

---

## ⚡ Anti-Patterns & Expert Traps

### 1. Deep Inheritance Trees
If your class hierarchy is 6 levels deep, it's a **Fragile Base Class**! A tiny change in the root class can break everything below. Focus on **Composition** (putting one object inside another) instead.

### 2. The "Everything is a Class" Trap
Python is multi-paradigm. Don't create a class if a simple function or dictionary will do. A class with only one method is just an expensive function!

---

## 🎯 Top 20 Principal Interview Questions (Object-Oriented Programming)

1. **Q: What is the difference between an 'Instance Attribute' and a 'Class Attribute'?**
   - **Answer**: An **Instance Attribute** is unique to each object (stored in `self`). A **Class Attribute** is shared by **Every** object created from that class.
2. **Q: Explain 'MRO' (Method Resolution Order).**
   - **Answer**: It is the order in which Python searches for a method in a class hierarchy (especially in multiple inheritance). It follows the **C3 Linearization algorithm**.
3. **Q: What is the purpose of `super()` and how is it different in Python 3 vs 2?**
   - **Answer**: `super()` allows you to call methods from a parent class or the next class in the **MRO**. In Python 3, you can just call `super().method()`, whereas Python 2 required passing the class and instance.
4. **Q: What is an 'Abstract Base Class' (ABC)?**
   - **Answer**: A blueprint that **cannot be instantiated**. It exists only to define a standard for its children to follow (using `@abstractmethod`).
5. **Q: Explain the difference between `__init__` and `__new__`.**
   - **Answer**: `__new__` is the actual creator of the object (it returns the instance). `__init__` is the initializer (it sets the data on the already-created instance).
6. **Q: What are `__slots__` and why are they used in high-performance systems?**
   - **Answer**: They tell Python to use a fixed-size array instead of a dynamic dictionary to store attributes. This results in **60-80% less memory usage** and slightly faster attribute access.
7. **Q: What is 'Polymorphism' in Python?**
   - **Answer**: The ability of different classes to be treated as instances of the same class through the same interface (e.g., calling `.save()` on both a `User` and an `Admin` object).
8. **Q: Explain 'Encapsulation' and Python's naming conventions.**
   - **Answer**: It's the grouping of data and methods into a single unit and limiting direct access. `_attr` is a "Protected" convention; `__attr` is "Private" (triggers name mangling).
9. **Q: What is 'Name Mangling'?**
   - **Answer**: When you use a double underscore `__my_var`, Python changes the internal name to `_ClassName__my_var` to prevent accidental overwriting in sub-classes.
10. **Q: What is the difference between 'Composition' and 'Inheritance'?**
    - **Answer**: **Inheritance** is an "Is-A" relationship (A Cat is an Animal). **Composition** is a "Has-A" relationship (A Car has an Engine). Experts favor Composition because it's more flexible.
11. **Q: What are 'Dunder' (Double-Underscore) or 'Magic' methods?**
    - **Answer**: Special methods that allow you to customize Python's built-in behavior (e.g., `__len__` for `len()`, `__add__` for `+`).
12. **Q: What is the purpose of the `@classmethod` and `@staticmethod` decorators?**
    - **Answer**: `@classmethod` receives the **Class** as the first argument (cls). `@staticmethod` receives no special first argument—it's just a regular function that lives inside a class's namespace.
13. **Q: Can you perform 'Multiple Inheritance' in Python?**
    - **Answer**: Yes. A class can inherit from multiple parents. Python uses the **MRO** to determine which parent's method to use first.
14. **Q: What is a 'Mix-in' class?**
    - **Answer**: A small, specialized class that is designed to be "Mixed in" to other classes to provide specific, optional functionality (e.g., a `JsonSerializerMixin`).
15. **Q: Explain the 'Diamond Problem'.**
    - **Answer**: A situation in multiple inheritance where a class inherits from two parents that both inherit from the same grandparent. Python's MRO resolves this by ensuring the grandparent is only called once.
16. **Q: What is the `@property` decorator used for?**
    - **Answer**: To define a **Getter** method that can be accessed like a regular attribute, allowing for lazy calculation or data validation during access.
17. **Q: What is a 'Class Factory'?**
    - **Answer**: A function or method that returns a new class instance, often allowing you to choose which class to instantiate at runtime based on the input.
18. **Q: What is 'Dependency Injection' in OOP?**
    - **Answer**: The practice of "Injecting" an object's dependencies (like a database client) through the constructor rather than creating them inside the class, making the code much easier to test.
19. **Q: What happens if you define `__del__` (The Destructor)?**
    - **Answer**: It is called when an object is about to be destroyed (reference count hits zero). However, it is **unreliable** and should generally be avoided in favor of Context Managers.
20. **Q: What is the purpose of `isinstance()` vs `type()`?**
    - **Answer**: `isinstance(obj, Class)` returns True if the object is an instance of that class **or any of its children**. `type(obj) == Class` checks for the **Exact** class only.

---

[Previous: File I/O](07-file-io-serialization.md) | [Next: Functional Programming →](09-functional-programming.md)
