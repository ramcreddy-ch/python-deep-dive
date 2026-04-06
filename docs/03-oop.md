# 03. Object-Oriented Programming (OOP) — Production Deep Dive

> OOP in Python is flexible and permissive. Without strict discipline, small utility classes quickly degrade into untestable "God Classes." I've spent thousands of hours refactoring monolithic infrastructure codebases into decoupled, interface-driven components. This is how we build scalable OOP structures in platform engineering.

---

## 🔍 Structural Foundations

### Dunder Methods (Magic Methods)
Python's data model heavily relies on double-underscore methods. Implementing them elevates your classes from simple data containers to standard Python objects.

```python
class K8sNode:
    def __init__(self, name: str, ip: str, is_ready: bool):
        self.name = name
        self.ip = ip
        self.is_ready = is_ready

    # Controls how the object is represented in logs (CRITICAL for debugging)
    def __repr__(self):
        return f"<K8sNode(name={self.name}, ready={self.is_ready})>"

    # Allows equality comparisons based on data, not memory address
    def __eq__(self, other):
        if not isinstance(other, K8sNode):
            return NotImplemented
        return self.name == other.name and self.ip == other.ip
```

### Encapsulation and Properties
Python does not have true `private` or `protected` modifiers. We use `_single_underscore` as a convention to say "internal use only", and `@property` for getter/setter control.

```python
class DataPipeline:
    def __init__(self):
        # Convention: internal variable
        self._max_retries = 3 

    @property
    def max_retries(self):
        return self._max_retries

    @max_retries.setter
    def max_retries(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Retries must be a positive integer.")
        self._max_retries = value
```

---

## 🏭 Architecture Patterns for SRE & DevOps

### Interfaces and ABCs (Abstract Base Classes)
Dynamic typing allows "duck typing", but when building plugins for an automation framework, we need strict contracts. The `abc` module is our interface enforcement mechanism.

```python
from abc import ABC, abstractmethod
import boto3

# The Contract
class CloudProvider(ABC):
    @abstractmethod
    def launch_instance(self, instance_type: str) -> str:
        """Returns instance ID"""
        pass

# The Implementation
class AWSProvider(CloudProvider):
    def __init__(self):
        self.ec2 = boto3.client('ec2')

    def launch_instance(self, instance_type: str) -> str:
        res = self.ec2.run_instances(InstanceType=instance_type, MinCount=1, MaxCount=1)
        return res['Instances'][0]['InstanceId']

# Trying to instantiate incomplete classes fails early:
# class GCPProvider(CloudProvider): pass
# gcp = GCPProvider()  # TypeError! abstract method launch_instance not implemented
```

### Dataclasses and Pydantic (Modern State Management)
Writing `__init__`, `__repr__`, and `__eq__` manually is tedious and error-prone. Python 3.7 introduced `dataclasses`. But in MLOps and APIs, where data enters from JSON or YAML, we default to **Pydantic**.

```python
from pydantic import BaseModel, ConfigDict, Field

class ModelConfig(BaseModel):
    # Prevents arbitrary extra JSON fields from polluting configs
    model_config = ConfigDict(extra="forbid") 

    model_name: str
    batch_size: int = Field(gt=0, le=1024)   # Built-in validation limits!
    learning_rate: float = 0.001

# Auto-validates and coerces string "32" to int 32
cfg = ModelConfig(model_name="ResNet50", batch_size="32")
```

---

## 🤖 MLOps / AI Perspective

### Multiple Inheritance & Mixins
When extending PyTorch Lightning modules or Scikit-Learn estimators, mixins are the cleanest way to add functionality (like logging or specific evaluation routines) without deep, fragile inheritance trees.

```python
class MLflowLoggerMixin:
    """Mixin to inject standardized logging"""
    def log_metrics(self, accuracy: float, loss: float):
        import mlflow
        mlflow.log_metrics({"acc": accuracy, "loss": loss})

# Base model class logic
class BaseClassifier:
    def train(self):
        print("Training model...")

# The actual production class combining behaviors
class ProductionClassifier(BaseClassifier, MLflowLoggerMixin):
    def run_epoch(self):
        self.train()
        self.log_metrics(0.95, 0.01) # MRO resolves this to the Mixin
```

### The `__call__` Method
In ML, models are objects, but we use them like functions. This is achieved via `__call__`. 

```python
class InferencePipeline:
    def __init__(self, model_path):
        self.model = self._load_model(model_path)
        
    def _load_model(self, path):
        # Heavy loading logic here
        return lambda x: x * 2  # mock model
        
    # Allows instance to be called like a function: obj(data)
    def __call__(self, input_tensor):
        processed = self._preprocess(input_tensor)
        return self.model(processed)

pipe = InferencePipeline("/models/v1")
result = pipe(torch.tensor([1, 2, 3])) # Calls __call__ automatically
```

---

## 🎯 Senior Engineer Interview Questions

**Q1: How does Python determine method resolution in multiple inheritance scenarios?**
> **Answer:** Python uses the C3 Linearization algorithm to build the Method Resolution Order (MRO). You can inspect it by looking at `ClassName.__mro__`. It ensures a class always precedes its parents, and if a class has multiple parents, it keeps the order they are listed in the class definition. If Python detects a cyclical or conflicting inheritance graph, it throws a `TypeError` at class creation rather than failing silently later.

**Q2: What are `@classmethod` and `@staticmethod`? Give a real-world use case for each.**
> **Answer:** A `@classmethod` takes `cls` as the first argument, giving it access to class-level state. It is heavily used for "alternative constructors" (e.g., `Config.from_yaml("file.yml")` or `Config.from_json("file.json)`). A `@staticmethod` takes neither `self` nor `cls`. It's essentially a normal function that happens to logically belong within a class's namespace. I use them for domain-specific utility functions, like `PasswordHasher.generate_salt()`.

**Q3: We need to ensure that our global `DatabaseConnectionPool` only ever has one instance running in memory per process. How do we achieve this in Python?**
> **Answer:** We need a Singleton pattern. While there are a few ways, the most robust Pythonic approach is overriding the `__new__` method, which handles object creation before `__init__` handles initialization. 
> ```python
> class DBPool:
>     _instance = None
>     def __new__(cls, *args, **kwargs):
>         if not cls._instance:
>             cls._instance = super(DBPool, cls).__new__(cls)
>         return cls._instance
> ```
> Another approach is using a module-level variable, as Python module imports are naturally singletons.

**Q4: In Pydantic/Dataclasses, what is the difference between defining an attribute as `list` vs `list = Field(default_factory=list)`?**
> **Answer:** This is addressing the mutable default argument trap. If you define a field simply as `config: list = []`, all instances of the object will share the exact same list in memory. If one instance modifies it, it leaks to all other instances. Using `default_factory=list` tells Python/Pydantic to execute the `list()` function to generate a fresh, new, isolated list in memory every time a new instance is created.

---

[← Previous: Control Flow](02-control-flow-functions.md) | [Back to Index](../README.md) | [Next: Data Structures & Collections →](04-data-structures.md)
