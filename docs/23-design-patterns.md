# 23. Design Patterns & Architecture — Production Deep Dive

> Design patterns in Python differ drastically from Java/C++. Because Python has first-class functions, dynamic typing, and monkey patching, patterns like Strategy and Command are often reduced to simple function passing. Here is how we structure Enterprise-level platform code.

---

## 🔍 Creational Patterns

### The Factory Pattern
Used heavily in Multi-Cloud orchestrations to decouple object construction from business logic based on dynamic environment strings.

```python
from abc import ABC, abstractmethod

class BaseStorage(ABC):
    @abstractmethod
    def upload(self, file_path): pass
    
class AWSStorage(BaseStorage):
    def upload(self, file_path): print("Uploading to S3")

class AzureStorage(BaseStorage):
    def upload(self, file_path): print("Uploading to Blob")

# The Factory Logic
class StorageFactory:
    @staticmethod
    def get_storage(cloud_provider: str) -> BaseStorage:
        if cloud_provider.lower() == "aws":
            return AWSStorage()
        elif cloud_provider.lower() == "azure":
            return AzureStorage()
        raise ValueError(f"Unsupported cloud: {cloud_provider}")

# API Layer doesn't care which cloud is implemented
storage = StorageFactory.get_storage(os.getenv("CLOUD_PROVIDER"))
storage.upload("/data/metrics.csv")
```

### The Singleton Protocol
Previously handled in the OOP section, but critical for managing stateful boundaries like connection pools (`psycopg2/SQLAlchemy`), Redis clients, and Boto3 `Session` objects to prevent massive connection leakages under load.

---

## 🏭 Behavioral Patterns

### The Strategy Pattern
Rather than building massive conditional chains inside a class, we inject the algorithm at runtime. In Python, we can just pass functions, bypassing the need for complex interface classes.

```python
import pandas as pd

# The Strategies (Algorithms)
def fill_with_mean(df, column):
    return df[column].fillna(df[column].mean())

def fill_with_median(df, column):
    return df[column].fillna(df[column].median())

# The Context (Executer)
class MLDataPreprocessor:
    def __init__(self, imputation_strategy):
        # We store the function reference!
        self.impute = imputation_strategy
        
    def process(self, df, column):
        df[column] = self.impute(df, column)
        return df

# Inject behavior dynamically
preprocessor = MLDataPreprocessor(imputation_strategy=fill_with_median)
cleaned_df = preprocessor.process(raw_dataframe, "age")
```

### The Observer Pattern
Pivotal for reactive systems (Event-Driven Architecture). When Kafka commits a message, multiple independent subscribers react without tight coupling.

```python
class EventBus:
    def __init__(self):
        self._subscribers = []
        
    def attach(self, func):
        self._subscribers.append(func)
        
    def notify(self, event_data: dict):
        for func in self._subscribers:
            func(event_data)

# The Event loop
bus = EventBus()

# Independent modules subscribing
def log_metric(data): print(f"Metric logged: {data}")
def trigger_pagerduty(data): 
    if data.get('severity') == 'high': print("Calling SRE OnCall!")

bus.attach(log_metric)
bus.attach(trigger_pagerduty)

# The core platform triggers exactly once
bus.notify({"type": "node_crash", "severity": "high"})
```

---

## 🔧 Structural Patterns

### The Adapter Pattern
When modernizing legacy systems, you must normalize input/outputs so the new Platform SDK doesn't break. 

```python
# The legacy API we cannot change
class LegacyAWSAPI:
    def execute_request_vm_xml(self, xml_payload):
        return "<success>id-1234a</success>"

# The Adapter
class CloudAdapter:
    def __init__(self, legacy_client):
        self.client = legacy_client
        
    def provision_instance(self, dict_payload):
        # Translates modern python concepts to legacy requirements
        xml = self._convert_dict_to_xml(dict_payload)
        res = self.client.execute_request_vm_xml(xml)
        return self._parse_xml_id(res)

provider = CloudAdapter(LegacyAWSAPI())
# Modern pipeline continues unimpacted
instance_id = provider.provision_instance({"type": "t3.large"})
```

---

## 🎯 Senior Engineer Interview Questions

**Q1: Explain Dependency Injection (DI). How does a framework like FastAPI essentially enforce it?**
> **Answer:** Dependency Injection mandates that objects retrieve their dependencies (like DB connections or Auth clients) from an external provider rather than constructing them internally. High coupling makes testing impossible (because you can't swap a real DB for a mock DB). FastAPI strictly enforces DI via the `Depends()` parameter. If an endpoint requires `def get_users(db: Session = Depends(get_db)):`, the FastAPI engine automatically resolves, provisions, and injects the dependency at runtime. During Pytest, we simply mandate `app.dependency_overrides[get_db] = get_mock_db`.

**Q2: Implementing the Command Pattern involves encapsulating requests as objects. Give an SRE use case.**
> **Answer:** Batch processing of critical infrastructure operations. For example, applying K8s manifests, draining nodes, and restarting deployments. Each operation is wrapped in a Command class with an `execute()` and an `undo()` method. These commands are grouped into a queue list. An orchestrator iterates over `cmd.execute()`. If step 4 throws a `KubernetesApiException`, the orchestrator immediately catches it, reverses the iteration, and triggers `cmd.undo()` on steps 3, 2, and 1, ensuring the cluster safely reverts to its original topological state.

**Q3: Describe the Facade Pattern and how Cloud SDKs use it.**
> **Answer:** The Facade Pattern provides a simplified, higher-level interface covering a massively complex subsystem of classes. In cloud engineering, the Boto3 resource API (`boto3.resource('s3')`) is a facade. Under the hood, querying an S3 bucket involves initiating HTTP session handlers, orchestrating SigV4 cryptographic signing processes, implementing pagination tokens, and parsing XML network errors. The developer using the Facade simply writes `bucket.objects.all()`, entirely insulated from the internal routing chaos.

**Q4: Contrast horizontal scaling of Python microservices with scaling monolithic Python architectures. What structural state patterns block horizontal scaling?**
> **Answer:** Monoliths scale vertically (larger CPUs, more RAM) while Microservices scale horizontally (deploying multiple identical pod replicas behind a load balancer). If a Python architecture violates statelessness—such as relying on the Singleton pattern to store user session data/tokens in the local Python app's memory (`dict`), or writing raw files to the container's ephemeral `/tmp` filesystem—it blocks horizontal scaling. If Request 1 hits Replica A (and stores state), and Request 2 hits Replica B, the state is gone and the transaction fails. All state must be structurally pushed to external persistence (Redis/Memcached vs PostgreSQL).

---

[← Previous: Security](22-security.md) | [Back to Index](../README.md) | [Next: Packaging →](24-packaging.md)
