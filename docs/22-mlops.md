# 22. MLOps — Experiment Tracking, Model Serving & Pipelines

> "A model that lives in a Jupyter notebook is a science experiment. A model that lives in a production pipeline is a business asset. An expert doesn't just 'fit a model'; they use MLOps to automate the entire lifecycle from training to monitoring and deployment."

---

## ❓ The 'Why' (High-Level)
In traditional software, we only manage **Code**. In Machine Learning (ML), we manage **Code + Data + Hyperparameters**. This makes development 3x harder. **MLOps** (Machine Learning Operations) is the discipline of creating a repeatable and automated process for building, testing, and deploying ML models. A principal engineer knows that a "Stale" model is worse than "No" model.

---

## 🌱 Module 1: The Basics (Junior) — The Lifecycle
ML training is different because it is **Iterative**.

### 1. Training and Saving
You train a model and "Persist" it so it can be used later without retraining.
```python
import joblib
from sklearn.linear_model import LogisticRegression

model = LogisticRegression().fit(X_train, y_train)
# Save the model to a file
joblib.dump(model, "my_model.pkl")
```

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — Experiment Tracking
Mid-level engineers don't lose track of their experiments.

### 1. MLflow Tracking
If you run 50 experiments with different settings, how do you remember which one was best?
- **MLflow**: Automatically logs your parameters, metrics (Accuracy/F1), and the final model file.
```python
import mlflow

with mlflow.start_run():
    mlflow.log_param("alpha", 0.5)
    mlflow.log_metric("accuracy", 0.92)
    mlflow.log_model(model, "model")
```

---

## 🌳 Module 3: Advanced Mechanics (Senior) — Versioning & Serving
Senior engineers ensure that **Data** is versioned just like code.

### 1. Data Version Control (DVC)
Git is terrible for storing 10GB datasets. **DVC** stores a "Pointer" in Git while keep the actual data in an S3 bucket, ensuring that your model and the data it used are always linked.

### 2. Model Serving with FastAPI
A model is only useful if it's accessible via an API.
```python
from fastapi import FastAPI
app = FastAPI()

@app.post("/predict")
def predict(data: dict):
    return model.predict(data["features"])
```

---

## 🔥 Module 4: Principal Architect (Principal) — Production at Scale
At the highest level, you automate the "Re-training" process.

### 1. Model Registry & Drift Detection
- **Model Registry**: A central hub where models are "Promoted" from `Staging` to `Production` after passing automated tests.
- **Drift Detection**: What if people's buying habits change over time? A principal engineer monitors the model's accuracy in real-time. If it drops (**Drift**), the system automatically triggers a re-training pipeline.

### 2. GPU Optimization
For deep learning (PyTorch/TensorFlow), you must understand how to move data from **CPU RAM** to **GPU VRAM** efficiently using **CUDA**.

---

## 🏗️ Case Study: The Auto-Scaling Recommender
A streaming service needed to retrain their recommendation model every 24 hours on 500GB of new data.
- **The Junior Approach**: A manual cron job that a dev runs on their laptop. (Failed every time the dev was on vacation).
- **The Principal Approach**: Built an **ML Pipeline** in **Kubeflow**. When the pipeline finished, the model was automatically validated against a test set. If it surpassed the current production model's accuracy, it was "Soft-Deployed" as a **Shadow Model** (receiving real traffic but its results weren't seen by users) to verify its performance before going live.
- **Result**: Successfully automated 100% of the training process, reducing manual labor to **zero** and keeping recommendations fresh.

---

## ⚡ Anti-Patterns & Expert Traps

### 1. Hardcoding Model Paths
Never do `model = load('C:/users/name/model.pkl')`. Use **Environmental Variables** or an **Artifact Registry** (like S3 or MLflow).

### 2. Not Versioning Data
If you retrain your model and it fails, but you don't know which version of the data caused the failure, you are in big trouble. **Expert Fix**: Always use **DVC** or **Delta Lake** for versioned datasets.

---

## 🎯 Top 20 Principal Interview Questions (MLOps)

1. **Q: What is 'MLOps' and how is it different from DevOps?**
   - **Answer**: DevOps focuses on **Code**. MLOps adds the management of **Data** and **Model State**. MLOps must account for "Model Decay" (degrading performance over time), which doesn't exist in traditional software.
2. **Q: What is a 'Model Registry'?**
   - **Answer**: A central repository that stores trained models along with their metadata (who trained it, on what data, and its performance metrics). It facilitates the transition between development, staging, and production.
3. **Q: Explain 'Data Drift'.**
   - **Answer**: A situation where the statistical properties of the incoming production data change over time, making the model less accurate because it was trained on "different" data.
4. **Q: What is 'DVC' (Data Version Control)?**
   - **Answer**: A tool that versions your datasets and models by storing only a metadata pointer in Git and the actual large files in a cloud storage (like S3), allowing for complete reproducibility.
5. **Q: How does 'MLflow' help in experiment tracking?**
   - **Answer**: It provides an API and UI for logging all parameters, code versions, and metrics for every experiment run, allowing teams to compare results easily and find the best model.
6. **Q: What is a 'Feature Store'?**
   - **Answer**: A centralized library of "Features" (pre-calculated data points) that can be used by multiple models for both training and real-time inference, ensuring consistency.
7. **Q: Explain 'Model Serving' and common tools for it.**
   - **Answer**: The process of making a trained model available via an API. Common tools include **FastAPI** (for simple use), **Triton** (for high-speed GPU serving), and **Seldon Core** (for K8s).
8. **Q: What is 'A/B Testing' for ML models?**
   - **Answer**: Routing a small portion of traffic to a new model version and the rest to the old version to compare their real-world performance (e.g., click-through rate) before fully switching.
9. **Q: Explain the 'CI/CD/CT' loop in MLOps.**
   - **Answer**: **CI** (Integration), **CD** (Delivery), and **CT** (**Continuous Training**). CT is the unique part of MLOps where the system automatically retrains and redeploys models based on new data.
10. **Q: What is 'Model Explainability' (SHAP/LIME)?**
    - **Answer**: Tools and techniques used to understand **Why** a model made a specific prediction, which is critical for trust and for compliance in regulated industries like finance and healthcare.
11. **Q: How do you handle 'Imbalanced Datasets'?**
    - **Answer**: By using techniques like **Oversampling** the minority class, **Undersampling** the majority class, or using specialized loss functions that penalize errors on small classes more heavily.
12. **Q: What is 'Quantization' in model optimization?**
    - **Answer**: Reducing the precision of the model's numbers (e.g., from 32-bit floats to 8-bit integers). This makes the model much smaller and faster with only a tiny loss in accuracy.
13. **Q: What is a 'Directed Acyclic Graph' (DAG) in ML Pipelines?**
    - **Answer**: A logical flow of tasks (Data Prep -> Train -> Evaluate -> Deploy) where every step has a clear dependency and there are no circular loops.
14. **Q: Explain 'Cold Start' in model serving.**
    - **Answer**: The time it takes for a new model instance to load its large weight file (often gigabytes) into memory before it can begin answering requests.
15. **Q: What is the purpose of 'Hyperparameter Tuning' (e.g., Optuna)?**
    - **Answer**: Automatically searching for the best settings (like learning rate or tree depth) to get the highest possible accuracy from a model.
16. **Q: What is 'Inference Latency'?**
    - **Answer**: The time it takes for a model to receive an input and return a prediction. For real-time apps (like self-driving cars), this must be in milliseconds.
17. **Q: How do you monitor a model in production?**
    - **Answer**: By monitoring the **System metrics** (CPU/Latecny) and **Model metrics** (is the predicted distribution of values shifting far away from the training distribution?).
18. **Q: What is 'Transfer Learning'?**
    - **Answer**: Taking a pre-trained model (like GPT or ResNet) and "Fine-tuning" it on a small amount of your own specific data to get high performance without the cost of a full training run.
19. **Q: Explain 'Orchestration' (e.g., Kubeflow/Airflow).**
    - **Answer**: The system that manages the execution of your ML pipeline, handling retries, parallel task execution, and resource allocation (like requesting a GPU node).
20. **Q: Why is 'Reproducibility' the most important goal of MLOps?**
    - **Answer**: Because if you cannot recreate a model from scratch (using the same code and the same data), you cannot reliably debug it, improve it, or meet regulatory audit requirements.

---

[Previous: Data Engineering](21-data-engineering.md) | [Next: LLM Engineering →](23-llm-engineering.md)
