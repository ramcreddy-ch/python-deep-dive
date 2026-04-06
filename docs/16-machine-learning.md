# 16. Machine Learning — Numpy, Scikit-Learn & PyTorch Deep Dive

> Training a model in a Jupyter Notebook is easy. Deploying that model into a high-throughput, low-latency, deterministic production environment is where most ML projects fail. We must understand exactly how Python bridges high-level algorithms to low-level C++ and CUDA matrices.

---

## 🔍 NumPy: The Foundation of all Tensors

Every ML framework (PyTorch, TensorFlow, Scikit-Learn) relies on the underlying concepts defined by NumPy: C-contiguous memory arrays.

### Broadcasting
Broadcasting allows operations on arrays of different shapes without manually creating `for` loops or duplicating data in memory. Master this, and your code speeds up 100x.

```python
import numpy as np

# Shape (3, 1) Matrix
user_features = np.array([[10], [20], [30]]) 
# Shape (4,) Vector
weights = np.array([0.1, 0.2, 0.3, 0.4])    

# Broadcasting magically stretches the (3, 1) to (3, 4) 
# and the (4,) to (3, 4) implicitly in C-memory to perform element-wise mult
result = user_features * weights 

print(result.shape) # Output: (3, 4)
```

### Memory Views vs Copies
A massive source of silent memory bloat in ML processing.

```python
arr = np.arange(1_000_000)

# This creates a VIEW (pointer). Modifying `slice_arr` modifies `arr`! Zero RAM cost.
slice_arr = arr[100:500] 

# This creates a hard COPY. Massive RAM cost if done repeatedly.
filtered_arr = arr[arr > 50000] 
```

---

## 🏭 Scikit-Learn: Architecting Pipelines

In production, models act on raw data. If your training script preprocesses data manually with Pandas, and you don't save those transformation states (mean, stdev, one-hot encodings), your inference server will fail (Data Leakage/Drift).

**Always use `sklearn.pipeline`**. It serializes the data transformations *with* the model.

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
import joblib

# Deterministic preprocessing layout
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['age', 'income']),
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['city', 'job'])
    ])

# Single executable pipeline artifact
production_model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100))
])

# Fit BOTH the scalers and the model simultaneously
production_model.fit(X_train, y_train)

# Pickle the entire pipeline. The inference server simply calls model.predict(raw_json)
joblib.dump(production_model, 'model_v1.pkl')
```

---

## 🚀 PyTorch: Deep Learning on Hardware

PyTorch constructs computational graphs dynamically (Define-by-Run) using Autograd. 

### The `nn.Module` Standard
Everything is a module. State (weights) sits in `self.parameters()`.

```python
import torch
import torch.nn as nn

class FraudDetector(nn.Module):
    def __init__(self, input_dim):
        super().__init__() # Must call parent initializer
        self.network = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.2), # Dropout behaves differently in train() vs eval() mode!
            nn.Linear(64, 1),
            nn.Sigmoid()
        )
        
    def forward(self, x):
        """The computational forward pass definition"""
        return self.network(x)

model = FraudDetector(input_dim=10)
# Send weights to GPU memory
model = model.to('cuda') 
```

### Inference Mode (Critical for latency)
During inference, computation graphs are useless. Disabling them saves ~30% GPU RAM and dramatically boosts speed.

```python
# MLOps Inference Server Code
model.eval() # 1. Disables Dropout and freezes BatchNorm stats

@torch.no_grad() # 2. Turns off explicit Autograd graph tracking
@torch.inference_mode() # 3. PyTorch 1.9+: Even stricter no_grad for max performance
def predict(tensor_input):
    return model(tensor_input)
```

---

## 🎯 Senior Engineer Interview Questions

**Q1: Describe the vanishing gradient problem and how modern architectures solve it in PyTorch.**
> **Answer:** In deep network backpropagation, gradients are continually multiplied by the chain rule. If the derivatives of activation functions (like traditional Sigmoid) are < 1, the gradient shrinks exponentially, meaning early layers barely update their weights. Modern architectures solve this via 1) ReLu activations (derivative is purely 1 or 0), 2) Batch Normalization (keeps outputs centered in non-saturating regions), and 3) Residual/Skip connections (ResNet), which supply an alternative additive path allowing gradients to flow backwards unimpeded.

**Q2: We need to put a PyTorch transformer model into production for a real-time API. Raw PyTorch is too slow. How do we optimize it?**
> **Answer:** Normal Python PyTorch runs through the heavy CPython interpreter dynamically. We must compile it down to an optimized static graph. We would use `torch.jit.script` (TorchScript) or the newer `torch.compile` (PyTorch 2.0+) to fuse internal operations. For strict hardware optimization, we would export the model to ONNX, and run it using the ONNX Runtime or NVIDIA TensorRT, which aggressively optimize matrix multiplications for the specific target GPU architecture, bypassing Python entirely.

**Q3: What does `optimizer.zero_grad()` do in a PyTorch training loop, and what happens if you forget it?**
> **Answer:** PyTorch explicitly *accumulates* gradients in the `.grad` attributes of tensor leaves upon every `loss.backward()` call, rather than replacing them. This is intended to support gradient accumulation for large logical batch sizes. If you enter the next batch loop and forget to call `optimizer.zero_grad()`, the new gradients are added mathematically to the gradients of the previous batch, pointing the optimizer in nonsensical directions and destroying model convergence immediately.

**Q4: In Scikit-Learn, how do you prevent Data Leakage during hyperparameter tuning (GridSearchCV)?**
> **Answer:** Data Leakage happens when information from the validation fold bleeds into the training phase. If you run a `StandardScaler.fit_transform()` on the entire dataset *before* passing it into `GridSearchCV`, the scaler has learned the mean/variance of the hold-out validation tests! You prevent this by encapsulating the Scaler explicitly inside an `sklearn.pipeline.Pipeline`, and passing the *complete pipeline* to the GridSearch. This forces the grid search to recalculate the scaling logic strictly on the N-1 internal folds at every step.

---

[← Previous: Data Engineering](15-data-engineering.md) | [Back to Index](../README.md) | [Next: MLOps →](17-mlops.md)
