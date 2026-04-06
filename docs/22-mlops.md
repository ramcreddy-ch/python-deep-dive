# 22. MLOps — MLflow, Model Serialization & Pipelines

> "A model is just a file until it's deployed. Expert MLOps engineers build the bridge between Data Science and SRE by using Python to automate model tracking, lifecycle management, and high-performance serving at scale."

---

## 🌱 The Basics: Training & Evaluation
The entry-level way to use machine learning in Python is to use **Scikit-Learn** or **PyTorch** locally.

```python
from sklearn.linear_model import LogisticRegression

# 1. Simple setup
model = LogisticRegression()
# model.fit(X_train, y_train)

# 2. Score check
# score = model.score(X_test, y_test)
# print(f"Model Accuracy: {score}")
```

---

## 🌿 Intermediate: Model Serialization (Pickle & Joblib)
After training a model, you must save it to disk for later use. This is "Serialization."

**Real Use (ML Engineering)**:
Saving a model from a training job and loading it in a separate inference API.

```python
import joblib

# 1. Save (Serialize)
# joblib.dump(model, "fraud_model.pkl")

# 2. Load (Deserialize)
# loaded_model = joblib.load("fraud_model.pkl")
# prediction = loaded_model.predict([[0.5, 1.2, -0.4]])
```

---

## 🌳 Advanced: Experiment Tracking (MLflow)
Senior engineers use **MLflow** to track every version of a model, the data it was trained on, and its accuracy.

**Real Use (MLOps)**:
A production-grade training script that records every parameter to a central server.

```python
import mlflow

def train_with_tracking():
    """
    Expert Pattern: Experiment Tracking. 
    Demonstrates: Versioning your models and results.
    """
    with mlflow.start_run():
        # Log parameters
        mlflow.log_param("n_estimators", 100)
        
        # Log metrics
        mlflow.log_metric("accuracy", 0.94)
        
        # Log the model artifact
        # mlflow.sklearn.log_model(model, "model_v1")
```

---

## 🔥 Expert: PyTorch & Distributed Models
Principal engineers use **PyTorch** to build deep learning models and distribute their training across many GPUs using **Horovod** or **Deepspeed**.

### 1. Tensors & Gradients
PyTorch uses **Tensors** (similar to NumPy arrays but they can live on a GPU) to perform high-speed matrix math.

### 2. The Model Lifecycle
Building a full automation pipeline: 
`Data Ingestion` -> `Training` -> `Validation` -> `Registry` -> `Serving`.

---

## 🎯 Top 20 Principal Interview Questions (MLOps)

1. **Q: What is the 'Model Lifecycle' in MLOps?**
   - **Answer**: The end-to-end process of **Data Ingestion** -> **Feature Engineering** -> **Training** -> **Validation** -> **Registration** -> **Deployment** -> **Monitoring**.
2. **Q: Explain 'Model Drift' and how to detect it.**
   - **Answer**: It is when the statistical property of the independent variables changes, making your model less accurate over time. We detect it by comparing live prediction results against training data distributions using **EvidentlyAI**.
3. **Q: Why is 'Versioning' mandatory for both Models and Data?**
   - **Answer**: Because a model's performance is tied to its data. To reproduce a result, you must know the **Exact Code**, the **Exact Parameters**, and the **Exact Data version** (using DVC) that produced it.
4. **Q: What is 'MLflow' and its core components?**
   - **Answer**: It is an open-source platform for the machine learning lifecycle. Core components: **Tracking** (logs), **Projects** (code format), **Models** (serialization), and **Registry** (versioning).
5. **Q: Explain 'Inference' and its two main types.**
   - **Answer**: **Real-Time Inference** (Single predictions via an API with low latency) and **Batch Inference** (Processing millions of rows at once on a schedule).
6. **Q: What is 'Pickle' vs 'ONNX' for model serialization?**
   - **Answer**: **Pickle** is Python-specific and insecure. **ONNX** (Open Neural Network Exchange) is a cross-language format that allows you to train in Python and run in C# or Java.
7. **Q: What is a 'Feature Store' (e.g., Feast)?**
   - **Answer**: A centralized repository used to store and serve features (data points) for both training and real-time inference, ensuring consistency across a large team.
8. **Q: Explain the 'CI/CD for ML' (CT - Continuous Training).**
   - **Answer**: The practice of automatically retraining a model when its performance drops or when new data arrives, without manual intervention.
9. **Q: What is 'Hyperparameter Tuning' and how is it automated?**
   - **Answer**: Searching for the best settings (like learning rate or number of layers) for a model. Automated using tools like **Optuna** or **Ray Tune**.
10. **Q: How do you serve a Python model as a high-performance API?**
    - **Answer**: Using **FastAPI** with a production server like **Uvicorn**, or a specialized tool like **NVIDIA Triton** or **Seldon Core**.
11. **Q: What is the purpose of 'DVC' (Data Version Control)?**
    - **Answer**: To treat large datasets like Git treats code. Instead of committing a 10GB CSV to Git, DVC stores the file in S3 and commits a small "Pointer" file to Git.
12. **Q: Explain 'Shadow Deployments' (A/B Testing).**
    - **Answer**: Capturing live traffic and sending it to both the old model and the new model simultaneously. The old model's result is used for the user, but the new model's result is logged for comparison.
13. **Q: What is the 'COLD START' problem in ML serving?**
    - **Answer**: The delay that occurs when a new model instance is started (e.g., loading a 5GB model into GPU memory) before it can serve its first request.
14. **Q: How do you handle 'Imbalanced Data' during training?**
    - **Answer**: Using techniques like **Oversampling** (adding more copies of rare items) or **SMOTE** (generating synthetic data) to ensure the model learns correctly from all classes.
15. **Q: What is a 'Tensor' in PyTorch/TensorFlow?**
    - **Answer**: A multi-dimensional array (like a Matrix) that is optimized for high-speed mathematical operations on a **GPU**.
16. **Q: Explain 'Overfitting' vs 'Underfitting'.**
    - **Answer**: **Overfitting**: The model learns the training data too perfectly but fails on new data. **Underfitting**: The model is too simple and fails to learn the patterns in the training data at all.
17. **Q: What is 'Quantization' in MLOps?**
    - **Answer**: Reducing the precision of model weights (e.g., from 32-bit to 16-bit or 8-bit) to make the model **faster** and **smaller** with minimal loss in accuracy.
18. **Q: What is the 'F1 Score' and why is it sometimes better than 'Accuracy'?**
    - **Answer**: The F1 score is a balance between **Precision** and **Recall**. It's better for imbalanced data (e.g., fraud detection where only 1% of transactions are fraud) because accuracy can stay at 99% while failing to find any actual fraud.
19. **Q: How do you perform 'Distributed Training' in PyTorch?**
    - **Answer**: Using **DistributedDataParallel (DDP)** or **Deepspeed** to split the training work across multiple GPUs or multiple servers.
20. **Q: What is 'Model Pruning'?**
    - **Answer**: The process of removing "unimportant" neurons or layers from a neural network to reduce its size and increase its speed without losing significant accuracy.

---

[← Previous: Data Engineering](21-data-engineering.md) | [Next: LLMOps →](23-llm-engineering.md)
