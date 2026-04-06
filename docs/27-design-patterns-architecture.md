# 27. Design Patterns & Architecture — Clean, SOLID & Modular Systems

> "A junior writes code that works. A senior writes code that can be changed. An expert writes systems that are 'Open for Extension but Closed for Modification'. Mastering design patterns is about building blueprints that stand the test of time and scale."

---

## 🌱 The Basics: SOLID Principles
At the entry level, we follow high-level design rules:

- **S (Single Responsibility)**: A class should have only ONE job.
- **O (Open/Closed)**: You should be able to add new functionality without editing existing code.
- **D (Dependency Inversion)**: Relies on abstractions (interfaces), not details.

---

## 🌿 Intermediate: Strategy & Factory Patterns
The **Strategy** pattern allowing you to switch between different "Engines" for a common interface.

```python
class StorageStrategy:
    def save(self, data): pass

class S3Storage(StorageStrategy):
    def save(self, data): print(f"Saving to S3: {data}")

class LocalStorage(StorageStrategy):
    def save(self, data): print(f"Saving to Disk: {data}")

class DataPipeline:
    def __init__(self, strategy: StorageStrategy):
        self.strategy = strategy

    def run(self, payload):
        self.strategy.save(payload)

# Usage: Changing behavior without changing the Pipeline code!
# pipeline = DataPipeline(S3Storage())
```

---

## 🌳 Advanced: Resilience (Circuit Breaker & Idempotency)
Senior engineers build "Self-Healing" systems.

**1. Circuit Breaker**: If a backend service is down, the code "Opens the Circuit" and fails immediately for 60 seconds instead of waiting for a 10s timeout every time.

**2. Idempotency**: Ensuring that running the same operation twice (e.g., a payment or a cloud creation) doesn't cause a double-charge or a double-resource.

```python
import time

def resilient_call(func):
    """
    Expert Pattern: Circuit Breaker Logic. 
    Demonstrates: Preventing 'Systemic Failure' by failing fast.
    """
    # ... logic to check failure count ...
    # if fail_count > 5:
    #    raise Exception("Circuit is Open. System is currently unstable.")
```

---

## 🔥 Expert: Config-Driven Systems (Pydantic-Settings)
Principal engineers avoid "Magic Numbers" in code. They use Type-Safe configuration systems.

**Real Use (Platform Engineering)**:
A system that loads infrastructure config from a YAML file or Env Vars and validates it instantly.

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Principal Pattern: Config Isolation. 
    Demonstrates: Centralizing all architecture config in one place.
    """
    app_name: str = "ML-Gateway"
    admin_email: str
    items_per_user: int = 50

    class Config:
        env_file = ".env"

# settings = Settings()
# print(settings.app_name)
```

---

## 🎯 Top 20 Principal Interview Questions (Design Patterns & Architecture)

1. **Q: What are the SOLID principles?**
   - **Answer**: **S**ingle Responsibility, **O**pen/Closed, **L**iskov Substitution, **I**nterface Segregation, **D**ependency Inversion. They are the 5 pillars of manageable software design.
2. **Q: Explain 'Dependency Injection' (DI) and why it is useful.**
   - **Answer**: The practice of "Injecting" external services (like a database or API client) into a class instead of creating them inside it. This makes the class **Loosely Coupled** and much easier to test with "Mocks."
3. **Q: What is the 'Strategy' pattern?**
   - **Answer**: Allowing an application to choose an algorithm or "behavior" (strategy) at runtime from a set of interchangeable options.
4. **Q: What is a 'Singleton' and why is it often called an 'Anti-Pattern'?**
   - **Answer**: A class that only allows one instance. It's often an anti-pattern because it introduces **Global State**, making the application harder to test and multi-thread.
5. **Q: Explain the 'Factory' pattern.**
   - **Answer**: A method or class designed to **Create Objects** without exposing the creation logic to the client. It abstractly returns an object of a shared base type.
6. **Q: What is 'Idempotency' in the context of REST APIs or Infrastructure scripts?**
   - **Answer**: The property where multiple identical requests have the same effect as a single request. Example: Making the same "Update" request 10 times doesn't change the state after the first one.
7. **Q: What is a 'Circuit Breaker' pattern and why is it used in Microservices?**
   - **Answer**: A stability pattern that "Opens" (stops requests) when an external service is detected to be failing. This prevents the primary application from hanging and allows the failing service to recover.
8. **Q: Explain 'Composition over Inheritance'.**
   - **Answer**: Favoring "Has-A" relationships (combining objects) instead of "Is-A" (class hierarchies). It leads to more modular and flexible systems.
9. **Q: What is 'Event-Driven Architecture' (EDA)?**
   - **Answer**: A design where components communicate asynchronously by producing and consuming **Events** (e.g., using Kafka or SQS), allowing for high-scale decoupled systems.
10. **Q: What is 'Domain-Driven Design' (DDD)?**
    - **Answer**: An architectural approach that centers the design around the **Business Domain** and its rules, using a shared language between developers and business experts.
11. **Q: What is 'Loose Coupling'?**
    - **Answer**: Designing components so they have minimal knowledge of each other. Changes in one component should not require changes in others.
12. **Q: Explain 'Microservices' vs 'Monolithic' architecture.**
    - **Answer**: **Monolith**: One big app (easy to build, hard to scale). **Microservices**: Many small apps (hard to build, easy to scale and deploy independently).
13. **Q: What is the 'Observer' pattern?**
    - **Answer**: A design where an object (the subject) maintains a list of dependents (observers) and notifies them automatically of any state changes (e.g., pub/sub).
14. **Q: What is 'Command Query Responsibility Segregation' (CQRS)?**
    - **Answer**: The pattern of using different models for **Reading** data (Queries) and **Writing** data (Commands) to optimize Performance and Security.
15. **Q: Explain the 'Adapter' pattern.**
    - **Answer**: A "Wrapper" that allows two incompatible interfaces to work together. It translates the interface of one class into an interface the client expects.
16. **Q: What is 'Refactoring'?**
    - **Answer**: Improving the **Internal Structure** of the code without changing its **External Behavior**. It's key to keeping technical debt low.
17. **Q: What is a 'Service Mesh' (e.g., Istio) and how does Python interact with it?**
    - **Answer**: An infrastructure layer for handling service-to-service communication, including load balancing, security, and observability. Python apps interact via sidecar proxies.
18. **Q: Explain 'State Management' in large Python applications.**
    - **Answer**: Managing how the "Truth" of the app is stored (e.g., in a central Database, Redis cache, or an internal Singleton).
19. **Q: What is 'Database Normalization' vs 'Denormalization'?**
    - **Answer**: **Normalization**: Reducing duplication (saving space). **Denormalization**: Intentionally adding duplication to **speed up reads** (common in high-scale systems).
20. **Q: What is 'Technical Debt' and how do you manage it?**
    - **Answer**: The implied cost of additional rework caused by choosing an easy (but messy) solution now instead of a better approach that would take longer. Managed by regular refactoring and "Debt-only" sprints.

---

[← Previous: Metaprogramming](26-metaprogramming-descriptors.md) | [Next: Database Engineering →](28-database-engineering.md)
