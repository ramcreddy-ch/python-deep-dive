# 08. Object-Oriented Programming — Classes, Inheritance & Composition

> "A class isn't just a container for data. To be an expert, you must understand that OOP is about 'Encapsulation' and 'Polymorphism' — building blueprints that allow your system to grow without breaking."

---

## 🌱 The Basics: Classes & Objects
A **Class** is the blueprint; an **Object** is the actual house built from that blueprint.

- **`__init__`**: The "Constructor." This is where you set the initial state of the object.
- **`self`**: A reference to the specific object instance being created.

```python
class AppService:
    def __init__(self, name):
        self.name = name

    def start(self):
        print(f"Service {self.name} starting...")

# Instantiating (creating the object)
service = AppService("LogProcessor")
service.start()
```

---

## 🌿 Intermediate: Inheritance & Super()
Inheritance allows one class to "inherit" all the methods and attributes from another class. This is the foundation of DRY (Don't Repeat Yourself) code.

**Real Use (API/Platform)**:
A base "CloudClient" that specific "AWSClient" and "AzureClient" classes inherit from.

```python
class CloudClient:
    def __init__(self, region):
        self.region = region

    def connect(self):
        print(f"Connecting to {self.region}...")

class AWSClient(CloudClient):
    def __init__(self, region, access_key):
        # Call the parent's constructor
        super().__init__(region)
        self.access_key = access_key

    def connect(self):
        super().connect() # Perform parent logic
        print(f"Applying AWS Key: {self.access_key}")
```

---

## 🌳 Advanced: Properties & Encapsulation (@property)
An expert uses **Properties** to hide logic behind a simple attribute. This is "Encapsulation" in action — protecting the internal state of an object.

```python
class ServerConfig:
    """
    Expert Pattern: Encapsulation. 
    Demonstrates: Validation before setting values.
    """
    def __init__(self, cpu_cores):
        self._cpu_cores = cpu_cores

    @property
    def cpu_cores(self):
        # Getter
        return self._cpu_cores

    @cpu_cores.setter
    def cpu_cores(self, value):
        # Setter with validation!
        if value < 1:
            raise ValueError("CPU Cores must be at least 1!")
        self._cpu_cores = value
```

---

## 🔥 Expert: Composition over Inheritance
Principal engineers often prefer **Composition**. Instead of a class "Is a" something (Inheritance), it "Has a" something (Composition). 

**Real Use (MLOps)**:
A "ModelServer" that *has* a "Predictor" and *has* a "Logger", rather than inheriting from both.

---

## 🎯 Top 20 Principal Interview Questions (OOP)

1. **Q: What is the difference between a 'Class' and an 'Object'?**
   - **Answer**: A **Class** is the template/blueprint. An **Object** is the real instance created in memory from that class.
2. **Q: What is the purpose of `self`?**
   - **Answer**: It represents the **Current Instance** being worked on. It allows the Python interpreter to distinguish between attributes of different objects created from the same class.
3. **Q: Explain 'Encapsulation' in Python.**
   - **Answer**: Hiding the internal state of an object and only allowing access through public methods or **Properties**. Use `_var` (convention) or `__var` (name mangling) for "Private" attributes.
4. **Q: What is the difference between `__init__` and `__new__`?**
   - **Answer**: `__new__` is the **Constructor** (it creates the empty object). `__init__` is the **Initializer** (it takes the created object and fills it with data).
5. **Q: What is 'Polymorphism'?**
   - **Answer**: The ability of different classes to respond to the **same method name**. Example: Both `AWSClient` and `AzureClient` have a `.connect()` method, but their implementations are different.
6. **Q: What is 'Multiple Inheritance' and how is it handled?**
   - **Answer**: It's when a class inherits from more than one parent. Python uses the **MRO (Method Resolution Order)** via the C3 Linearization algorithm to decide which method to call first.
7. **Q: What is a '@classmethod' vs a '@staticmethod'?**
   - **Answer**: `@classmethod` takes **the class itself** (`cls`) as an argument. Use it for "Alternative Constructors" (e.g., `User.from_json()`). `@staticmethod` takes no extra arguments and is just a function grouped inside a class for organization.
8. **Q: Why use `super()` instead of explicitly calling the parent class?**
   - **Answer**: `super()` automatically handles the **MRO** in complex inheritance trees, ensuring each parent is called only once and in the correct order (avoiding the 'Diamond Problem').
9. **Q: What is an 'Abstract Base Class' (ABC)?**
   - **Answer**: A class that cannot be instantiated. It's used as a "Protocol" (blueprint) to force children to implement certain methods (e.g., every `Database` class must implement `.query()`).
10. **Q: What is 'Composition over Inheritance'?**
    - **Answer**: Favoring "Has-A" relationships instead of "Is-A". Instead of complex inheritance, you build a class by combining simpler, smaller objects. This makes the code much more modular.
11. **Q: What are 'Dunder' (Double Under) methods?**
    - **Answer**: Built-in methods like `__str__`, `__len__`, or `__add__` that allow your custom classes to behave like standard Python types (e.g., allowing you to add two objects with `+`).
12. **Q: What is the difference between `__str__` and `__repr__`?**
    - **Answer**: `__str__` is for users (readable). `__repr__` is for developers (detailed, ideally allowing you to recreate the object).
13. **Q: How can you prevent a class from being inherited?**
    - **Answer**: Python doesn't have a 'final' keyword. However, you can use a **Metaclass** to throw an error if a child tries to inherit from it.
14. **Q: What is 'Name Mangling' in Python?**
    - **Answer**: Using `__attribute` (double underscore) changes the internal name of the attribute to `_Class__attribute` to prevent accidental overwriting by children.
15. **Q: What is the purpose of `@property`?**
    - **Answer**: To turn a method into a **Getter** that looks like an attribute. It allows you to add validation logic (in the **Setter**) while keeping the public API simple.
16. **Q: What is the 'Diamond Problem' in inheritance?**
    - **Answer**: When Class D inherits from B and C, which both inherit from A. If A has a method overridden by B and C, which one does D use? Python's MRO solves this.
17. **Q: What is an 'Interface' in Python?**
    - **Answer**: Python uses **Abstract Base Classes** (ABCs) or **Protocols** (PEP 544) to define interfaces.
18. **Q: Can you define a class inside a function?**
    - **Answer**: Yes. A "Local" class is only accessible within that function.
19. **Q: What is the `__dict__` attribute?**
    - **Answer**: A dictionary that stores all an object's instance attributes.
20. **Q: How do you check if an object is an instance of a specific class?**
    - **Answer**: Use `isinstance(obj, ClassName)`. Never use `type(obj) == ClassName` as it doesn't handle inheritance correctly.

---

[← Previous: File I/O](07-file-io-serialization.md) | [Next: Functional Programming →](09-functional-programming.md)
