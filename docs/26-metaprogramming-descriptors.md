# 26. Advanced OOP: Metaclasses & Descriptors — Internal Magic

> "Classes are actually just objects. To be a true expert, you must understand how Python's 'Class Factory' (Metaclasses) works and how 'Descriptors' power everything from `@property` to high-performance ORMs like SQLAlchemy."

---

## 🌱 The Basics: Class vs Instance
At the entry level, we know a **Class** is the template and an **Instance** is the actual data.

```python
class Profile:
    # Class-level attribute
    # Shared by ALL profiles
    platform = "GitHub"

    def __init__(self, name):
        # Instance-level attribute
        # Unique to THIS profile
        self.name = name

p1 = Profile("Ramchandra")
```

---

## 🌿 Intermediate: Descriptors (The `__get__` & `__set__` Protocol)
A **Descriptor** is an object that controls its own access. This is how `@property` is actually built.

```python
class PositiveNumber:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError(f"{self.name} cannot be negative!")
        instance.__dict__[self.name] = value

class Server:
    # Use the Descriptor
    cpu = PositiveNumber("cpu")

# s = Server()
# s.cpu = 4  # OK
```

---

## 🌳 Advanced: Metaclasses (`type`)
A **Metaclass** is the "Class that creates classes." By default, `type` is the metaclass.

**Real Use (Library Engineering)**:
Building a framework (like Pydantic or Django) that automatically turns class attributes into database columns.

```python
class GuardMeta(type):
    """
    Expert Pattern: Class Validation. 
    Demonstrates: Preventing a class from being created if it's missing a field.
    """
    def __new__(cls, name, bases, dct):
        if "id" not in dct and name != "BaseModel":
            raise TypeError(f"Class {name} must have an 'id' attribute!")
        return super().__new__(cls, name, bases, dct)

# This will work
class BaseModel(metaclass=GuardMeta): pass

# This will FAIL with a TypeError!
# class User(BaseModel): pass
```

---

## 🔥 Expert: Dynamic Class Creation
Principal engineers use `type()` to create classes on-the-fly based on JSON config files or API schemas.

```python
# Expert Pattern: Dynamic Schema. 
# 1. Read JSON config.
# 2. Extract fields.
# 3. Create the class without code!
DynamicUser = type("DynamicUser", (object,), {"id": 1})
```

---

## 🎯 Top 20 Principal Interview Questions (Metaprogramming & Descriptors)

1. **Q: What is a Metaclass in Python?**
   - **Answer**: It is a 'Class Factory' — the class that creates other classes. By default, `type` is the metaclass for all objects in Python.
2. **Q: What is the difference between `__new__` and `__init__` in a Metaclass?**
   - **Answer**: `__new__` is called when the class is **not yet created**; it allows you to modify the class attributes before it's born. `__init__` is called after the class has been created.
3. **Q: What is a 'Descriptor'?**
   - **Answer**: An object that implements `__get__`, `__set__`, or `__delete__`. It allows you to customize what happens when you access an attribute (e.g., validation, logging, or lazy loading).
4. **Q: How does `@property` actually work under the hood?**
   - **Answer**: It is a built-in **Data Descriptor** that maps attribute access to specific getter and setter functions.
5. **Q: When would you use a Metaclass over a Class Decorator?**
   - **Answer**: Use a **Decorator** to modify one specific class. Use a **Metaclass** when you want to modify a whole **Hierarchy** of classes (like every model in an ORM).
6. **Q: What is the purpose of `type(name, bases, dict)`?**
   - **Answer**: It is the dynamic way to create a class at runtime. `name` is the string name, `bases` is a tuple of parents, and `dict` is the dictionary of attributes/methods.
7. **Q: What is 'Duck Typing' vs 'Monkey Patching' in Metaprogramming?**
   - **Answer**: **Duck Typing**: Checking if an object has the methods you need. **Monkey Patching**: Dynamically adding or replacing those methods on an object at runtime.
8. **Q: Explain `__getattr__` vs `__getattribute__`.**
   - **Answer**: `__getattribute__` is called for **every** attribute access. `__getattr__` is called only if the attribute **doesn't exist** normally.
9. **Q: What is the 'MRO' (Method Resolution Order)?**
   - **Answer**: The order in which Python looks for a method in a class hierarchy (using the C3 Linearization algorithm). View it with `MyClass.__mro__`.
10. **Q: What is the benefit of using `__slots__`?**
    - **Answer**: It prevents the creation of a `__dict__` for instances, significantly reducing memory usage for classes with millions of objects.
11. **Q: What is a 'Non-Data Descriptor'?**
    - **Answer**: A descriptor that only implements `__get__`. If an instance has an attribute with the same name, the instance attribute will take precedence.
12. **Q: What is a 'Data Descriptor'?**
    - **Answer**: A descriptor that implements both `__get__` and `__set__`. It will **always** take precedence over an instance attribute of the same name.
13. **Q: How do you implement a 'Singleton' pattern using a Metaclass?**
    - **Answer**: By overriding the `__call__` method in the metaclass to keep a reference to the first instance and always return it.
14. **Q: What is the purpose of `__init_subclass__`?**
    - **Answer**: A simpler alternative to metaclasses for performing actions whenever a child class is created (added in Python 3.6).
15. **Q: Can you change the metaclass of a class after it's been created?**
    - **Answer**: **No**. The metaclass is baked into the class at creation time.
16. **Q: What is 'Attribute Access Shadowing'?**
    - **Answer**: When an instance attribute hides a class attribute of the same name.
17. **Q: How does SQLAlchemy use Metaclasses?**
    - **Answer**: To automatically map class attributes (like `name = Column(...)`) to database columns and handle the underlying SQL generation.
18. **Q: What is the 'Abstract Base Class' (ABC) and how does it use metaclasses?**
    - **Answer**: ABCs use the `ABCMeta` metaclass to enforce that children must implement specific "Abstract" methods before they can be instantiated.
19. **Q: What is a 'Class Factory' function?**
    - **Answer**: A function that returns a new class dynamically: `def make_class(name): return type(name, (Base,), {})`.
20. **Q: How can you prevent an attribute from being deleted?**
    - **Answer**: By implementing the `__delete__` method in a descriptor to raise an `AttributeError`.

---

[← Previous: Security](25-advanced-security.md) | [Next: Design Patterns →](27-design-patterns-architecture.md)
