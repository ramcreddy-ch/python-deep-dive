# 17. MLOps — MLflow, Kubeflow & Model Serving Deep Dive

> Training a model is data science. Operating a model continuously across retraining loops, handling schema drift, maintaining inference latency, and tracking hyperparameter lineage is MLOps. This is where classical Software Engineering meets Statistical Models.

---

## 🔍 Experiment Tracking (MLflow)

In a Jupyter Notebook, if you change a parameter and overwrite the variable, the old model's exact context is lost forever. MLflow is the industry standard for logging experiment lineage, ensuring 100% reproducibility.

### The Autolog Pattern
Instead of writing 50 lines of boilerplate `log_metric()`, modern MLflow handles this natively via patching.

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier

# Configure remote tracking server (Runs as a pod in K8s)
mlflow.set_tracking_uri("http://mlflow-server.platform.svc.cluster.local:5000")
mlflow.set_experiment("fraud_detection_v2")

# Magical auto-logging patches Scikit-learn methods
mlflow.sklearn.autolog()

with mlflow.start_run(run_name="rf_estimators_200"):
    # This single call natively logs:
    # 1. All hyperparameters (n_estimators, max_depth, etc)
    # 2. Output metrics (accuracy, precise, recall)
    # 3. Model artifacts (Pickled model files)
    # 4. Git commit hash, Python version, pip dependencies (requirements.txt)
    model = RandomForestClassifier(n_estimators=200, max_depth=10)
    model.fit(X_train, y_train)
    
    # We can still add custom tags
    mlflow.set_tag("dataset_version", "v1.4.2")
```

### The Model Registry Transition
Once an experiment completes successfully, MLflow acts as the artifact repository. We promote ML models like we promote Docker images.

```python
# Transition model via Python API to Staging
client = mlflow.tracking.MlflowClient()
client.transition_model_version_stage(
    name="fraud_detection_model",
    version=3,
    stage="Staging",
    archive_existing_versions=True
)
```

---

## 🏭 Orchestration (Kubeflow Pipelines)

cronjobs cannot manage complex ML workflows because Steps 1 (ETL) and Step 2 (Training) require totally different compute (CPU vs. GPU arrays). Kubeflow natively translates Python code into a Kubernetes Argo DAG.

```python
import kfp
from kfp import dsl

# Define a step. Kubeflow packages this Python function into a Docker container 
# and runs it as a distinct Kubernetes Pod when executed.
@dsl.component(base_image='python:3.9', packages_to_install=['pandas'])
def preprocess_data(raw_data_path: str, preprocessed_path: str):
    import pandas as pd
    df = pd.read_csv(raw_data_path)
    df.fillna(0, inplace=True)
    df.to_csv(preprocessed_path, index=False)

@dsl.component(base_image='pytorch/pytorch:latest')
def train_model(data_path: str) -> str:
    # Model training logic...
    return "s3://models/v2/"

# Define the DAG (Directed Acyclic Graph)
@dsl.pipeline(name="Weekly Fraud Retraining")
def ml_pipeline(input_path: str = "s3://data/raw.csv"):
    
    # Data passing creates the dependency graph implicitly
    prep_task = preprocess_data(raw_data_path=input_path, preprocessed_path="/tmp/clean.csv")
    
    # This pod won't spawn until prep_task finishes. It automatically requests GPUs.
    train_task = train_model(data_path=prep_task.outputs['preprocessed_path'])
    train_task.set_gpu_limit(2) 

# Compile to a YAML Argo Workflow representation for Kubernetes
kfp.compiler.Compiler().compile(ml_pipeline, 'pipeline.yaml')
```

---

## 🚀 Model Serving (Triton / Seldon)

Serving models with Flask/FastAPI is fine for internal tools. In production scale-out, a Python REST API cannot batch incoming dynamic tensors across a single GPU memory bus efficiently. We rely on inference engines like Triton Inference Server or KServe.

Often, we just need a Python wrapper to send strict GRPC payloads to Triton.

```python
import tritonclient.grpc as grpcclient
import numpy as np

# GRPC bypasses HTTP serialization overhead (JSON parsing)
client = grpcclient.InferenceServerClient(url="triton.platform.local:8001")

# Construct native tensor payload
input_data = np.random.randn(1, 3, 224, 224).astype(np.float32)
inputs = [grpcclient.InferInput("IMAGE", input_data.shape, "FP32")]
inputs[0].set_data_from_numpy(input_data)

# High performance inferencing
results = client.infer(model_name="resnet50", inputs=inputs)
predictions = results.as_numpy("PROBABILITIES")
```

---

## 🎯 Senior Engineer Interview Questions

**Q1: In an MLOps context, explain the difference between Concept Drift and Data Drift. How do we detect them in Python?**
> **Answer:** *Data Drift* is when the statistical distribution of the incoming inputs (features) changes relative to the training set (e.g., age demographics skew younger). The model's logic is fine, but the inputs are weird. *Concept Drift* is when the statistical relationship between the input and the target variable changes (e.g., due to inflation, the model's mapping of "income -> loan default likelihood" is no longer accurate). We detect these by logging inference inputs/outputs via asynchronous message queues (Kafka), and calculating the Kolmogorov-Smirnov (KS) test or Population Stability Index (PSI) offline against the training baseline daily.

**Q2: We deployed a Python ML inference FastAPI endpoint. Under peak load, CPU usage is 100%, but GPU usage stays at barely 15%. What is the architectural bottleneck?**
> **Answer:** The bottleneck is Python's ability to shuttle data to the GPU and small batch sizes. Sending a single image through the entire network stack, parsing the JSON payload, moving the tensor to VRAM, computing, and returning is heavily IO/CPU bound. The GPU computes the single matrix math in a fraction of a millisecond and sits idle waiting for the next API request. The fix is implementing Dynamic Batching (natively supported by servers like Triton); the server holds incoming requests in a micro-queue for 10ms, slams 32 of them together into a single large tensor, and pushes *one* massive Matrix operation to the GPU, saturating it efficiently.

**Q3: Describe standard strategies for caching ML features in production to reduce prediction latency.**
> **Answer:** During training, we extract features from a data warehouse (Snowflake/BigQuery). In production, extracting those features (like "user's last 30 day purchase tally") in real-time from an SQL DB is too slow. We must implement an Online Feature Store (like Feast). The batch ETL process computes features and loads them into a fast, in-memory KV store (Redis). The Python inference API receives a `user_id`, queries Redis for the pre-computed features in <1ms, concats them with real-time payload features, and executes the prediction.

**Q4: How does MLflow handle dependency management when you deploy a logged model to an endpoint?**
> **Answer:** When MLflow logs a model (e.g., using `mlflow.sklearn.log_model`), it silently captures the specific Python environment. It creates an `MLmodel` file and a `conda.yaml` (or `requirements.txt`). This dictates the exact scikit-learn version, python version, and system dependencies present during training. When MLflow is commanded to serve the model (`mlflow models serve`), it reads those YAML files, provisions a perfectly matched virtual environment (or Docker container) on the fly, and fires up a Gunicorn/Waitress server running the model natively to prevent version-mismatch API crashes.

---

[← Previous: Machine Learning](16-machine-learning.md) | [Back to Index](../README.md) | [Next: LLMOps →](18-llmops.md)
