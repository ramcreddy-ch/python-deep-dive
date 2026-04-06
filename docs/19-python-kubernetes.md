# 19. Python for Kubernetes — Clients, CRDs & Custom Operators

> "Kubernetes is the 'Operating System' of the modern cloud. Every principal engineer understands that if you isn't automating Kubernetes through its API, you're doing it wrong. An expert uses Python to build 'Operators' that manage the entire lifecycle of a complex application, from DB migrations to scaling."

---

## ❓ The 'Why' (High-Level)
Kubernetes (K8s) is an ocean of resources—Pods, Services, Ingresses, and Secrets. While `kubectl` is great for humans, it's terrible for automation. **Python's Kubernetes Client** allows you to programmatically control your entire infrastructure. A principal engineer knows that the real power of K8s is in its extensibility—using Python to build **Custom Operators** that make a cluster "Self-Healing" and "Smart."

---

## 🌱 Module 1: The Basics (Junior) — The Python Client
You need to talk to the K8s API server.

### 1. The Survival Kit: Listing Pods
First, authenticate using your local `~/.kube/config` file.
```python
from kubernetes import client, config

config.load_kube_config()
v1 = client.CoreV1Api()
# List all pods in all namespaces
for pod in v1.list_pod_for_all_namespaces().items:
    print(pod.metadata.name)
```

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — Managing State
Mid-level engineers create, update, and delete resources.

### 1. CRUD on Deployments
Deployments manage the actual "Copies" of your application.
```python
from kubernetes import client
apps_v1 = client.AppsV1Api()
# Scale a deployment to 5 replicas
body = {"spec": {"replicas": 5}}
apps_v1.patch_namespaced_deployment_scale("my-app", "default", body)
```

### 2. Labels & Selectors
Always filter resources using **Labels** to avoid affecting the wrong application.

---

## 🌳 Module 3: Advanced Mechanics (Senior) — Watching & Executing
Senior engineers use the API for real-time monitoring and interactivity.

### 1. Watching Events
Instead of a slow loop, use a **Watch** object to get notified the second a resource changes.
```python
from kubernetes import watch
w = watch.Watch()
for event in w.stream(v1.list_pod_for_all_namespaces):
    print(f"Event: {event['type']}, Pod: {event['object'].metadata.name}")
```

### 2. Executing Commands in Pods
Sometimes you need to run a "Health Check" script inside a container from your Python script.

---

## 🔥 Module 4: Principal Architect (Principal) — Building Operators
At the highest level, you treat the **K8s API as your Framework**.

### 1. The Kubernetes Operator Pattern (Kopf)
An **Operator** is a Python script that "Watches" for a custom resource (e.g., a `PostgresDB` object) and handles the actual creation and maintenance of the database.
- **Framework**: Use **`Kopf`** (Kubernetes Operator Framework) to write operators easily.
```python
import kopf

@kopf.on.create('mycompany.com', 'v1', 'myobjects')
def create_fn(spec, **kwargs):
    print(f"I should create something with {spec}!")
```

### 2. Reconciliation & Finalizers
- **Reconciliation**: If someone manually deletes a pod, your operator sees the "Current State" doesn't match the "Desired State" and fixes it automatically.
- **Finalizers**: A mechanism that prevents a resource from being deleted until your Python script says it's ok (e.g., to perform a final backup).

---

## 🏗️ Case Study: The Auto-Scaling ML Cluster
A data science company was wasting $50,000 a month on idle GPU nodes.
- **The Junior Approach**: A cron job that looks for empty nodes and kills them. (Dangerous; sometimes nodes are just starting up). 
- **The Principal Approach**: Built a **Kubernetes Operator** in Python using `Kopf`. It listened for "Job" events. When a Job was submitted, the operator added a GPU node. When the job finished, the operator drained the node and terminated the instance.
- **Result**: Reduced GPU costs by **$40,000 per month** and ensured zero downtime for the researchers.

---

## ⚡ Anti-Patterns & Expert Traps

### 1. Hardcoding Namespaces
Never assume your app is in the `default` namespace. Always use environmental variables to let the orchestrator tell you where you are.

### 2. Ignoring 409 Conflict Errors
If two scripts try to update the same resource at the same time, K8s will return a **409 Conflict**. **Expert fix**: Use "Optimistic Concurrency Control" (checking the `resourceVersion`) or simply retry the update.

---

## 🎯 Top 20 Principal Interview Questions (Kubernetes Operators)

1. **Q: What is the 'Kubernetes Operator' pattern?**
   - **Answer**: it is an application-specific controller that extends the Kubernetes API to create, configure, and manage instances of complex applications automatically.
2. **Q: How does the `kubernetes` Python client authenticate in production?**
   - **Answer**: By using `config.load_incluster_config()`. This uses the ServiceAccount token mounted into the pod's file system by Kubernetes.
3. **Q: What is a 'CRD' (Custom Resource Definition)?**
   - **Answer**: It is a way to define your own "Object" in Kubernetes (like a `Database` or a `KafkaCluster`), allowing you to use `kubectl` and the API to manage them just like Pods.
4. **Q: What is a 'Reconciliation Loop'?**
   - **Answer**: The core logic of a controller or operator that continuously compares the **Desired State** (what's in ETCD) to the **Actual State** (what's in the cluster) and makes the necessary changes to align them.
5. **Q: Explain 'Finalizers' in Kubernetes.**
   - **Answer**: They are string keys that tell Kubernetes to not delete a resource until specific cleanup logic (handled by an operator) has been completed.
6. **Q: What is 'Informers' and 'Watches'?**
   - **Answer**: A **Watch** is a long-lived HTTP connection to receive events. An **Informer** is a higher-level abstraction that maintains a local cache of resources based on a Watch, improving performance.
7. **Q: What is the purpose of 'Owner References'?**
   - **Answer**: To tell Kubernetes that one resource (e.g., a Pod) "Belongs" to another (e.g., a Deployment). This allows for **Cascading Deletion** — if you delete the owner, K8s automatically deletes the children.
8. **Q: How do you handle 'Concurrency Conflicts' (Error 409) during updates?**
   - **Answer**: By implementing a **Retry Loop** that grabs the latest `resourceVersion` from the API server and attempts the update again with the new version.
9. **Q: What is 'Kopf'?**
   - **Answer**: A high-level Python framework designed specifically for building Kubernetes operators by annotating functions to respond to resource events.
10. **Q: Explain 'Namespacing' in the Python client.**
    - **Answer**: Resources in Kubernetes are either **Namespaced** (like Pods) or **Cluster-scoped** (like Nodes and Namespaces). Different API methods are used for each (e.g., `list_namespaced_pod` vs `list_node`).
11. **Q: What is the `v1` vs `AppsV1` vs `NetworkingV1` API levels?**
    - **Answer**: These are different **API Groups**. Core resources (Pods, S3) are in `v1`. Orchestration resources (Deployments) are in `apps/v1`. Networking (Ingress) is in `networking.k8s.io/v1`.
12. **Q: How can you stream logs from a pod using Python?**
    - **Answer**: By calling `read_namespaced_pod_log()` with the `follow=True` and `_preload_content=False` parameters, allowing you to iterate over the log lines as they arrive.
13. **Q: What is 'Optimistic Concurrency Control' in K8s?**
    - **Answer**: A strategy where updates only succeed if the resource hasn't been changed by someone else since you last read it (verified by the `resourceVersion` field).
14. **: What is 'Sidecar Container'?**
    - **Answer**: A second container running in the same Pod as your main app, often used for logging, monitoring, or proxying network traffic (like Istio/Envoy).
15. **Q: How do you manage K8s Secrets safely in Python?**
    - **Answer**: Secrets are **Base64 encoded**, NOT encrypted, in ETCD by default. When reading them in Python, you must decode them (`base64.b64decode`) to get the actual value.
16. **Q: What is 'Taints and Tolerations'?**
    - **Answer**: A mechanism to prevent pods from being scheduled on certain nodes (Taints) unless those pods explicitly state they can handle it (Tolerations).
17. **Q: Explain 'Affinity and Anti-Affinity'.**
    - **Answer**: Rules that tell Kubernetes "Put these pods together" (Affinity) or "Keep these pods on different servers" (Anti-Affinity) for performance or high-availability reasons.
18. **Q: What happens if your Operator crashes?**
    - **Answer**: Nothing happens to the resources it was managing. Once the operator restarts, it will trigger its reconciliation loop and "Catch up" on any events it missed.
19. **Q: What is `kubectl exec` and how do you do it in Python?**
    - **Answer**: It opens a websocket connection to a pod to run a shell command. The Python client provides the `stream()` utility to handle this complex interaction.
20. **Q: Why is Python a good choice for Operators compared to Go?**
    - **Answer**: While Go is the "Native" language of K8s, Python is much faster to write and has better integration with data science and DevOps tools (Boto3, Ansible), making it ideal for "Infrastructure Automation."

---

[Previous: SRE & Observability](18-python-sre-observability.md) | [Next: Python for CI/CD →](20-python-ci-cd.md)
