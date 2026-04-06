# 27. Design Patterns & SOLID — Scalable Architecture

> "A design pattern is a 'Battle-Tested' solution to a common software problem. An expert doesn't reinvent the wheel; they use Patterns to build systems that are 'Easy to Change' and 'Impossible to Break'. Mastering SOLID and Patterns is the difference between a coder and a Software Architect."

---

## ❓ The 'Why' (High-Level)
Software is never finished—it is constantly changing. If your code is a "Jumbled Mess," a tiny change to the login screen might break the payment system. **Design Patterns** provide a common language and a set of blueprints that keep your code organized. **SOLID** is the set of rules that ensure your code remains **Flexible**, **Maintainable**, and **Testable**.

---

## 🌱 Module 1: The Basics (Junior) — The Core Patterns
The most basic patterns help you manage how objects are created.

### 1. The Singleton (The "Only One")
Ensuring a class only ever has **one** instance (e.g., a database connection).
```python
class Database:
    _instance = None
    def __new__(cls):
        if cls._instance is None: cls._instance = super().__new__(cls)
        return cls._instance
```

### 2. The Factory (The "Creator")
Instead of the user deciding which class to create, a "Factory" function does it based on input.

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — The SOLID Principles
Mid-level engineers follow the 5 golden rules of architecture.

### 1. S - Single Responsibility
A class should have **one, and only one**, reason to change. (Don't put "user logic" and "email logic" in the same class!).

### 2. O - Open/Closed
Code should be **Open for extension** but **Closed for modification**. If you want to add a new payment method, you shouldn't have to change the old checkout code; you should just add a new class.

### 3. D - Dependency Inversion
High-level modules shouldn't depend on low-level modules; they should both depend on **Interfaces**. (Your app shouldn't "Talk to MySQL"—it should "Talk to a Database Interface").

---

## 🌳 Module 3: Advanced Mechanics (Senior) — Structural Patterns
Senior engineers manage how classes interact with each other.

### 1. The Observer (Pub/Sub)
Allows multiple objects (Observers) to "Listen" to another object (Subject). When the subject changes, all listeners are updated automatically. (Common in UI and messaging apps).

### 2. The Adapter
Allows two incompatible interfaces to work together. If your system expects an `Account` but the new bank API gives you a `Profile`, you write an "Adapter" to bridge the gap.

---

## 🔥 Module 4: Principal Architect (Principal) — Enterprise Patterns
At the highest level, you manage the "Flow" of data across the entire system.

### 1. The Repository & Unit of Work
- **Repository**: Decouples the "Domain logic" from the "Database logic." Your app just says `get_user(id)`, and doesn't care if it comes from SQL, a Cache, or an API.
- **Unit of Work**: Ensures that multiple database changes either **All succeed** or **All fail** (Atomic transaction).

### 2. Dependency Injection (DI)
Instead of a class "Creating" its own dependencies, they are "Injected" from the outside. This makes the code 100% testable with "Mock" objects.

---

## 🏗️ Case Study: Refactoring the "God Class"
A startup had a `SystemManager` class that was 5,000 lines long and handled everything from user login to PDF generation.
- **The Junior Approach**: Add `if / else` statements to the 5,000-line file. (Code became unreadable).
- **The Principal Approach**: Used **SOLID** to break the God class into 10 small, specialized classes. Used the **Strategy Pattern** to handle different types of PDF generation separately.
- **Result**: Reduced the bug rate by **80%** and allowed 5 developers to work on different parts of the system at the same time without "stepping on each other's toes."

---

## ⚡ Anti-Patterns & Expert Traps

### 1. The "Golden Hammer"
If you learn a new pattern (like a Factory), don't try to use it everywhere. A pattern that doesn't solve a real problem just makes your code slower and harder to read.

### 2. Complexity for the Sake of Complexity
Never use a pattern if a simple function will do. If your code can be solved in 10 lines of simple logic, don't write 3 classes and an interface just to follow a pattern.

---

## 🎯 Top 20 Principal Interview Questions (Design Patterns & SOLID)

1. **Q: What does the 'S' in SOLID stand for and why is it important?**
   - **Answer**: **Single Responsibility Principle**. It means a class or function should have only one reason to change, which makes it easier to understand, test, and maintain.
2. **Q: Explain the 'Open/Closed' Principle.**
   - **Answer**: Software entities should be open for **Extension** (adding new features) but closed for **Modification** (changing existing code). This prevents "regression" bugs when you add new things.
3. **Q: What is the 'Singleton' pattern and when should you avoid it?**
   - **Answer**: it's a pattern that ensures only one instance of a class exists. You should avoid it when it becomes a "Global Variable" that makes testing difficult.
4. **Q: What is 'Dependency Injection' (DI)?**
   - **Answer**: The practice of "Injecting" a class's dependencies (e.g., a database client) through its constructor rather than creating them inside. This allows for easy swapping of real objects for "Mocks" during testing.
5. **Q: Explain the 'Strategy' pattern.**
   - **Answer**: A behavioral pattern that allows you to define a family of algorithms and swap them at runtime. For example, a `PaymentProcessor` that can swap between `CreditCard` and `PayPal` strategies.
6. **Q: What is the 'Liskov Substitution Principle' (LSP)?**
   - **Answer**: It states that objects of a superclass should be replaceable with objects of its subclasses without breaking the application. A "Square" is usually NOT a "Rectangle" in LSP because it breaks the rectangular property of width/height independence.
7. **Q: What is the 'Observer' pattern?**
   - **Answer**: A behavioral pattern where an object (the subject) maintains a list of its dependents (observers) and notifies them automatically of any state changes.
8. **Q: Explain the 'Interface Segregation' Principle.**
   - **Answer**: Clients should not be forced to depend on methods they do not use. It's better to have many small, specific interfaces than one large, "fat" interface.
9. **Q: What is the 'Factory Method' pattern?**
   - **Answer**: A creational pattern that provides an interface for creating objects in a superclass but allows subclasses to alter the type of objects that will be created.
10. **Q: What is the 'Adapter' pattern?**
    - **Answer**: A structural pattern that allows two incompatible interfaces to work together. It acts as a "bridge" or "middle-man" between two disparate systems.
11. **Q: What is the 'Facade' pattern?**
    - **Answer**: A structural pattern that provides a **Simplified Interface** to a complex library, framework, or set of classes.
12. **Q: Explain 'Composition over Inheritance'.**
    - **Answer**: The architectural advice that it's better to build objects by "Having" other objects rather than "Being" a child of another class. This leads to more flexible and decoupled systems.
13. **Q: What is the 'Command' pattern?**
    - **Answer**: A behavioral pattern that turns a request or action into an object, allowing you to "Queue" actions, log them, or perform "Undo" operations.
14. **Q: What is a 'Mock' vs a 'Stub' in testing?**
    - **Answer**: A **Stub** provides canned answers (e.g., returns 200 OK). A **Mock** also checks if the code "behaved" correctly (e.g., "Was the `save()` method called exactly once?").
15. **Q: What is the 'Dependency Inversion' Principle?**
    - **Answer**: High-level modules (business logic) should not depend on low-level modules (database calls). Both should depend on **Abstractions (Interfaces)**.
16. **Q: What is the 'Repository' pattern?**
    - **Answer**: A pattern that hides the details of data storage (SQL, API, Cache) from the domain logic, providing a clean "List-like" interface for managing objects.
17. **Q: Explain the 'Decorator' pattern.**
    - **Answer**: A structural pattern that allows behavior to be added to an individual object, dynamically, without affecting the behavior of other objects from the same class.
18. **Q: What is the 'State' pattern?**
    - **Answer**: A behavioral pattern that allows an object to change its behavior when its internal state changes. The object will appear to change its class.
19. **Q: What is the 'Unit of Work' pattern?**
    - **Answer**: A pattern that tracks all changes to data during a single transaction and "commits" them all at once at the end, ensuring database consistency.
20. **Q: How can you implement a 'Circuit Breaker' pattern?**
    - **Answer**: By creating a wrapper around a network call that tracks failures. If failures pass a certain threshold, the breaker "Trips" and immediately returns an error for all future calls to prevent overwhelming the target system.

---

[Previous: Metaprogramming](26-metaprogramming.md) | [Next: Database Engineering →](28-database-engineering.md)
