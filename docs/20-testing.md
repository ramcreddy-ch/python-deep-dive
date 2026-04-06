# 20. Testing — Pytest, Mocking & TDD Deep Dive

> "Untestable code is broken code." In platform engineering, you cannot randomly deploy code to an AWS production account to "see if it works." Dynamic languages fail dynamically. Comprehensive test suites using Pytest fixtures and architectural mocking are mandatory.

---

## 🔍 Pytest: The Golden Standard

The built-in `unittest` module is clunky and heavily Java-influenced. Pytest relies on clean, raw `assert` statements combined with execution introspection.

### Fixtures: Managing State
Fixtures abstract setup/teardown logic. They inject dependencies directly into test functions based on type signatures.

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# scope="session" means this fixture runs ONCE for the entire test suite run
@pytest.fixture(scope="session")
def db_engine():
    """Sets up an isolated, temporary SQLite DB in memory"""
    engine = create_engine("sqlite:///:memory:")
    # Base.metadata.create_all(engine)
    yield engine 
    engine.dispose()

# Runs freshly BEFORE every single test function that requests it
@pytest.fixture(scope="function")
def db_session(db_engine):
    """Provides a fresh transactional session, rolled back after test"""
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    # TEARDOWN: Runs AFTER the test function yields back
    session.rollback()
    session.close()

# The test naturally receives the session object
def test_create_user(db_session):
    user = User(name="admin")
    db_session.add(user)
    db_session.commit()
    
    found = db_session.query(User).filter_by(name="admin").first()
    assert found is not None
```

---

## 🏭 Mocking External Dependencies

When testing Cloud/SRE scripts, you cannot actually provision a real Kubernetes cluster or an S3 bucket during a CI `git push`. We mock the boundaries.

### 1. `unittest.mock.patch`
Used to intercept and perfectly mimic external function calls and responses.

```python
from unittest.mock import patch, MagicMock
from infrastructure.aws_manager import purge_s3_bucket

# @patch replaces the 'boto3.client' inside 'aws_manager' module with a Mock
@patch('infrastructure.aws_manager.boto3.client')
def test_s3_purge_logic(mock_boto):
    # Retrieve the mock instance returned by the mocked client()
    mock_s3 = mock_boto.return_value
    
    # Configure the mock to return a fake API response
    mock_s3.list_objects_v2.return_value = {
        'Contents': [{'Key': 'log1.txt'}, {'Key': 'log2.txt'}]
    }

    # Execute business logic
    deleted_count = purge_s3_bucket("my-bucket")

    # Assertions on the mock's call history
    assert deleted_count == 2
    mock_s3.delete_object.assert_any_call(Bucket="my-bucket", Key="log1.txt")
```

### 2. Moto (Boto3 Mocker)
For AWS specifically, mocking every AWS response dictionary manually takes years. `moto` spins up a virtual, ephemeral mock AWS environment completely intercepting all `boto3` network calls.

```python
import boto3
from moto import mock_aws

@mock_aws
def test_aws_infrastructure():
    # Because of the decorator, this hits a local, fake AWS simulation!
    s3 = boto3.client('s3', region_name='us-east-1')
    
    s3.create_bucket(Bucket="test-bucket")
    s3.put_object(Bucket="test-bucket", Key="config.yaml", Body=b"debug: true")
    
    body = s3.get_object(Bucket="test-bucket", Key="config.yaml")['Body'].read()
    assert body == b"debug: true"
```

---

## 🔧 TDD inside MLOps & LLMOps

How do you "test" a probabilistic model that behaves differently every time?

### 1. Deterministic Seeding
You must freeze the pseudo-random number generators before loading models.

```python
import pytest
import numpy as np
import torch
import random

@pytest.fixture(autouse=True) # Runs automatically for all tests
def set_seeds():
    np.random.seed(42)
    random.seed(42)
    torch.manual_seed(42)
    torch.cuda.manual_seed_all(42)  # Critical for GPU ops!
```

### 2. Output Bounding
You don't test for exact numerical matches. You test for logical thresholds, shape constraints, and tensor gradients.

```python
def test_neural_network_forward_pass():
    model = NeuralNet(input_dim=10)
    mock_inputs = torch.randn(32, 10) # Batch of 32
    
    outputs = model(mock_inputs)
    
    # 1. Shape validation
    assert outputs.shape == (32, 1)
    
    # 2. Mathematical constraint validation (Sigmoid out must be 0-1)
    assert torch.all(outputs >= 0.0)
    assert torch.all(outputs <= 1.0)
    
    # 3. Gradient linkage validation
    outputs.mean().backward()
    
    for param in model.parameters():
        assert param.grad is not None, "Gradient graph is broken!"
```

---

## 🎯 Senior Engineer Interview Questions

**Q1: Explain the purpose of `patch.object` versus normal `patch`. Where does normal `patch` trip up junior engineers?**
> **Answer:** The biggest mistake with normal `patch('module.function')` is patching the target in the wrong namespace. If `app.py` imports `from auth import get_user`, patching `auth.get_user` does absolutely nothing during testing, because `app.py` has already bound that function into its local namespace. You must mock `app.get_user`. To avoid namespace confusion, `patch.object(AppClass, 'method_name')` allows you to explicitly target an instantiated object or class definition directly, and is significantly safer during refactoring.

**Q2: We have an `async def fetch_data()` method that queries a database and we want to write a Pytest test for it. How?**
> **Answer:** Standard Pytest relies on synchronous execution and does not manage an asyncio Event Loop, so calling an `async` function inside a standard `def test` returns an un-executed coroutine object. You must install the `pytest-asyncio` plugin. This allows you to write `pytest.mark.asyncio` above an `async def test_fetch_data()` test. The plugin orchestrates creating the event loop natively, awaiting your logic, and tearing it down safely.

**Q3: Describe Property-Based Testing using a library like `hypothesis`.**
> **Answer:** Standard TDD relies on the developer coming up with "Example-Based" examples (e.g., testing add logic with 1+1, 0+0, -1+1). Property-Based Testing flips this. You define the *properties* of the input (e.g., "The input is an array of random floats between 0 and 100") and the invariants of the output (e.g., "The output array must always be identical in length to the input array"). The `hypothesis` engine will autonomously generate tens of thousands of random edge-case inputs (empty lists, integers masquerading as floats, infinites, NaNs) and attempt to break your logic to find holes the engineer didn't conceive.

**Q4: We have an integration test suite that takes 45 minutes to run. How do you architect it to ensure unit tests execute fast on every commit?**
> **Answer:** Test segregation. In Pytest, you use marker decorators (`@pytest.mark.integration` or `@pytest.mark.slow`). In CI/CD build scripts for Pre-commit/Merge Requests, the action is configured to run `pytest -m "not integration"`. This executes only the highly-isolated, purely mocked unit tests in under 10 seconds. The full integration suite is deferred sequentially to nightly runs, or exclusively triggered prior to executing a deployment job into a Staging environment.

---

[← Previous: GPU Programming](19-gpu-programming.md) | [Back to Index](../README.md) | [Next: Performance Optimization →](21-performance.md)
