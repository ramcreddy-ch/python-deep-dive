# 26. Metaprogramming — Metaclasses, type() & Code Generation

> "Metaprogramming is 'Code that writes code.' An expert doesn't just use classes; they use Metaclasses to build powerful frameworks (like Django or SQLAlchemy) that handle all the repetitive boiler-plate code for you. If you understand Metaclasses, you understand the secret soul of Python."

---

## ❓ The 'Why' (High-Level)
In standard programming, you write a class to represent an object (like a User). But what if you have 100 different classes and they all need the same "validation" or "database" logic? Instead of copy-pasting code into each class, you write a **Metaclass** — a "class for classes." This allows you to automatically "inject" behavior into your code without the developer even seeing it.

---

## 🌱 Module 1: The Basics (Junior) — Reflection & Introspection
The first step is looking at an object's "Innards."

### 1. `getattr` and `setattr`
You can access or change an object's data using **Strings** instead of hardcoded names.
```python
class MyClass: pass

obj = MyClass()
setattr(obj, "name", "Ram")  # Same as obj.name = "Ram"
print(getattr(obj, "name")) # Same as print(obj.name)
```

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — Dynamic Creation
Mid-level engineers don't just "instantiate" classes; they **Create** them on the fly.

### 1. The `type()` function (The 3-argument version)
Did you know you can create a class without using the `class` keyword?
```python
# Create a class named 'User' that has a 'save' method
User = type("User", (object,), {"save": lambda self: print("Saved!")})
```

### 2. The `__dict__` attribute
Every object in Python stores its data in a simple dictionary called `__dict__`. If you change this dictionary, you change the object!

---

## 🌳 Module 3: Advanced Mechanics (Senior) — Intercepting Classes
Senior engineers use hooks to automatically change how their code behaves.

### 1. Metaclasses (Inheriting from `type`)
A Metaclass is a way to say "Every time a new class is created using this metaclass, run this code."
```python
class PluginMeta(type):
    def __new__(cls, name, bases, attrs):
        print(f"I found a new plugin: {name}!")
        return super().__new__(cls, name, bases, attrs)

class MyPlugin(metaclass=PluginMeta): pass  # Triggers the print!
```

### 2. `__init_subclass__` (The modern way)
Introduced in Python 3.6, this is a simpler and cleaner way to do 90% of what metaclasses do without the complexity of inheriting from `type`.

---

## 🔥 Module 4: Principal Architect (Principal) — The Magic Behind the Scenes
At the highest level, you manage how objects are "Born" and how they "Search" for data.

### 1. `__new__` vs `__init__`
- **`__new__`**: It is the actual creator of the object. It returns the instance (The "Allocation" step).
- **`__init__`**: It fills the created object with data (The "Initialization" step).
- **Principal Choice**: Use `__new__` to implement the **Singleton** pattern (meaning the class can only ever have ONE instance).

### 2. The Descriptor Protocol
Ever wonder how `@property` works? It's a **Descriptor**. It's an object that manages how another object's attribute is accessed. This is how high-performance frameworks handle "Lazy Loading" from a database.

---

## 🏗️ Case Study: The Auto-Validating ORM
A startup was processing millions of "Invoices", but half of them had "Incorrect Data" (missing totals, negative prices).
- **The Junior Approach**: Add a `validate()` function to every single model and call it manually every time. (Devs forgot to call it, and bugs continued).
- **The Principal Approach**: Created a **Metaclass** for all models. When a dev defined a field like `price = MoneyField(min=0)`, the metaclass automatically added validation logic to the `__setattr__` method of the class.
- **Result**: Data corruption dropped to **Zero**, as it was now "physically impossible" to save a bad invoice into the system.

---

## ⚡ Anti-Patterns & Expert Traps

### 1. Over-Metaprogramming
Metaprogramming makes code "Hidden." If you use too much of it, other developers will not understand how the system works. **Expert fix**: Use it only for "Generic Framework" code (like a Database library), never for "Business logic."

### 2. Confusing `__getattr__` and `__getattribute__`
- `__getattribute__` is called for **EVERY** access (Extremely slow and dangerous!).
- `__getattr__` is only called if the attribute is **Missing**. (Safe and efficient!).

---

## 🎯 Top 20 Principal Interview Questions (Metaprogramming)

1. **Q: What is a Metaclass in Python?**
   - **Answer**: it is a "Class for a Class." Just as a class is a blueprint for an object, a metaclass is the blueprint for the class itself.
2. **Q: What is the base metaclass for all classes in Python?**
   - **Answer**: **`type`**. Every class in Python 3 is an instance of `type`.
3. **Q: Explain the difference between `__new__` and `__init__`.**
   - **Answer**: `__new__` is the actual creator (constructor) that returns the instance. `__init__` is the initializer that sets up the data on the already created instance.
4. **Q: How do you create a class dynamically at runtime?**
   - **Answer**: By using the three-argument version of `type(name, bases, attributes_dict)`.
5. **Q: What is the purpose of `__init_subclass__`?**
   - **Answer**: Introduced in 3.6, it provides a lightweight way to customize class creation for children, avoiding the need for a full metaclass for most simple tasks.
6. **Q: What is the 'Descriptor Protocol'?**
   - **Answer**: A set of methods (`__get__`, `__set__`, `__delete__`) that allow an object to manage the attribute access of another object. This is how `@property` and `@staticmethod` work.
7. **Q: Explain the difference between `__getattr__` and `__getattribute__`.**
   - **Answer**: `__getattribute__` is called for every attribute access. `__getattr__` is only called as a fallback if the attribute is not found in the standard way.
8. **Q: How can you implement a 'Singleton' using `__new__`?**
   - **Answer**: By storing the instance in a class-level variable and returning that same instance every time `__new__` is called.
9. **Q: What are 'Abstract Base Classes' (ABCs)?**
   - **Answer**: They are classes that cannot be instantiated and are used to define a common interface (blueprint) that all subclasses must follow.
10. **Q: What is the 'MRO' (Method Resolution Order)?**
    - **Answer**: The order in which Python searches for a method in a class hierarchy, especially in multiple inheritance, following the C3 Linearization algorithm.
11. **Q: What does the `dir()` function return?**
    - **Answer**: A list of all attributes and methods available on an object, including inherited ones.
12. **Q: What is 'Duck Typing'?**
    - **Answer**: The philosophy of, "If it walks like a duck and quacks like a duck, it's a duck." It means Python cares about an object's **methods/behavior**, not its actual class type.
13. **Q: How do you prevent new attributes from being added to a class dynamically?**
    - **Answer**: By using `__slots__`, which restricts the attributes a class can have and saves memory by skipping the creation of the `__dict__`.
14. **Q: What is 'Monkey Patching'?**
    - **Answer**: Dynamically replacing a method or attribute of a class or module at runtime, often used for testing (mocking) or fixing bugs in third-party libraries.
15. **Q: Explain `__call__`.**
    - **Answer**: It allows an object to be **Called like a function**. If an object has a `__call__` method, you can do `my_obj()`.
16. **Q: What is the purpose of the `inspect` module in metaprogramming?**
    - **Answer**: It provides powerful tools for "introspection" — looking at real-time information about live objects like their source code, arguments, and stack frames.
17. **Q: How does the `@property` decorator use descriptors internally?**
    - **Answer**: It creates a descriptor object where the `fget` function is called when you read the attribute, and `fset` is called when you write to it.
18. **Q: What is 'introspection' vs 'reflection'?**
    - **Answer**: **Introspection**: Looking at the code from the inside (reading attributes). **Reflection**: Modifying the code from the inside (changing attributes/methods at runtime).
11. **Q: Can a class have more than one metaclass?**
    - **Answer**: No. A class can only have one direct metaclass. However, that metaclass can inherit from other metaclasses.
20. **Q: When should you NOT use metaprogramming?**
    - **Answer**: When a simpler solution like a **Function Decorator** or simple **Inheritance** can solve the problem. Metaprogramming adds significant complexity to debugging.

---

[Previous: Security](25-advanced-security.md) | [Next: Design Patterns →](27-design-patterns-solid.md)
