# 19. Python for Kubernetes — Clients, Controllers & Operators

> "Kubernetes is the 'Operating System' of the Cloud. Expert Platform Engineers use Python to extend Kubernetes — writing custom controllers, managing resources via the API, and building 'Self-Healing' operators that automate complex stateful applications."

---

## 🌱 The Basics: The Kubernetes Client
The entry-level way to talk to K8s from Python is via the **`kubernetes`** official client.

```python
from kubernetes import client, config

# 1. Load the cluster config (Works locally or inside a Pod)
config.load_kube_config()

# 2. List all Pods in the 'default' namespace
v1 = client.CoreV1Api()
# pods = v1.list_namespaced_pod(namespace="default")
# for pod in pods.items:
#     print(f"Pod: {pod.metadata.name}")
```

---

## 🌿 Intermediate: Dynamic Resource Management
Senior engineers don't just "List" resources; they **Update** and **Create** them dynamically based on external events.

**Real Use (Platform/Scaling)**:
Scaling a deployment to 10 replicas if a SQS queue has 1,000,000 messages.

```python
from kubernetes.client import AppsV1Api

def scale_deployment(name, replicas):
    """
    Expert Pattern: Auto-Scaling logic. 
    Demonstrates: Programmatically changing the cluster state.
    """
    api = AppsV1Api()
    # body = {"spec": {"replicas": replicas}}
    # api.patch_namespaced_deployment_scale(name, "default", body)
```

---

## 🌳 Advanced: Watchers & Events
Instead of "Polling" the API every 10 seconds, use a **Watcher**. It keeps a persistent connection open and alerts your Python script the **exact moment** a resource changes.

**Real Use (SRE/Logging)**:
A Python script that automatically alerts Slack the second any Pod in the cluster enters a `CrashLoopBackOff` state.

```python
from kubernetes import watch

def watch_pods():
    """
    Expert Pattern: Reactive Automation. 
    Demonstrates: Instant event handling in K8s.
    """
    v1 = client.CoreV1Api()
    w = watch.Watch()
    # for event in w.stream(v1.list_pod_for_all_namespaces):
    #     print(f"Event: {event['type']} Pod: {event['object'].metadata.name}")
```

---

## 🔥 Expert: Building Orperators (Kopf)
Principal engineers build **Kubernetes Operators**. They use a framework like **`Kopf`** to write "Handers" that respond to custom events (CRDs).

```python
import kopf

@kopf.on.create('my-api.com', 'v1', 'myresources')
def create_fn(spec, **kwargs):
    """
    Principal Pattern: Operator Logic. 
    1. A developer creates a 'MyResource' YAML.
    2. Python automatically creates a DB, an S3 bucket, and a Secret.
    """
    print(f"Creating infrastructure for {spec.get('name')}")
```

---

## 🎯 Top 20 Principal Interview Questions (Kubernetes & Python)

1. **Q: How does the Python K8s client handle authentication inside a Pod?**
   - **Answer**: Using `config.load_incluster_config()`. It automatically looks for the ServiceAccount token and CA certificate at `/var/run/secrets/kubernetes.io/serviceaccount/`.
2. **Q: What is the difference between `list_namespaced_pod` and `list_pod_for_all_namespaces`?**
   - **Answer**: The first only sees one namespace. The second requires a **ClusterRole** with cluster-wide permissions to see every pod in the entire cluster.
3. **Q: Explain 'Patch' vs 'Replace' in the K8s API.**
   - **Answer**: `Replace` (PUT) requires the **Whole** resource object and overwrites it. `Patch` (PATCH) only sends the **Specific Fields** you want to change (e.g., just the replicas).
4. **Q: What is a 'Watcher' and why is it more efficient than 'Polling'?**
   - **Answer**: A **Watcher** uses a long-lived HTTP connection. The server "Pushes" updates to Python instantly. This is much faster and puts less load on the API server than polling every few seconds.
5. **Q: What is a 'Custom Resource Definition' (CRD)?**
   - **Answer**: It allows you to define your own API objects in Kubernetes (e.g., `MyDatabase` instead of just `Deployment`). Python can then "Watch" and "Manage" these custom objects.
6. **Q: What is a 'Kubernetes Operator'?**
   - **Answer**: A specialized Python application that "Operates" a complex piece of software (like a database or a mesh) by watching its CRDs and taking automated actions to keep it healthy.
7. **Q: Explain the 'Kopf' framework.**
   - **Answer**: It is a high-level Python library for writing Kubernetes Operators that handles the low-level "Watching" and "Syncing" logic, allowing you to focus on the actual business automation.
8. **Q: How do you handle 'API Throttling' when managing 1,000+ pods?**
   - **Answer**: By using **Paginators** and **Caching**. Never list all pods every second; use a **Watcher** to maintain a local, in-memory cache of the cluster state.
9. **Q: What is 'Owner References' in K8s?**
   - **Answer**: It's a way to link resources. If you delete a parent object, Kubernetes will automatically delete all its "Children" (e.g., deleting a Deployment deletes its Pods).
10. **Q: How do you read a 'Secret' from Python in K8s?**
    - **Answer**: Either by reading it as an **Environment Variable** (standard) or by using the `CoreV1Api` to fetch the secret object directly and decoding the base64 data.
11. **Q: What is a 'Liveness Probe' and a 'Readiness Probe'?**
    - **Answer**: **Liveness**: "Am I healthy?" (K8s restarts if it fails). **Readiness**: "Am I ready for traffic?" (K8s stops traffic if it fails).
12. **Q: Explain 'Annotation' vs 'Label'.**
    - **Answer**: **Labels** are for **Selecting** objects (identifying). **Annotations** are for **Attaching metadata** (description, instructions) that doesn't need to be indexed for fast searching.
13. **Q: What is 'Informers' and why are they used?**
    - **Answer**: An optimized caching layer that watches a resource and maintains a local "Mirror" of the cluster state in RAM for instant, zero-latency access by your Python code.
14. **Q: How do you handle 'Concurrent Updates' (Conflict errors)?**
    - **Answer**: K8s uses **Optimistic Concurrency Control**. Every resource has a `resourceVersion`. If you try to update an old version, you get a **409 Conflict**. You must re-read the object and try again.
15. **Q: What is the 'Kubelist' and 'KubePod' data structure in the client?**
    - **Answer**: They are the Python objects returned by the API that map directly to the JSON/YAML structure of the Kubernetes resource.
16. **Q: How do you scale a 'StatefulSet' via Python?**
    - **Answer**: Using the `AppsV1Api` and patching the `replicas` field of the StatefulSet object.
17. **Q: What is 'Namespace Isolation'?**
    - **Answer**: It allows you to group resources. A Python script can be restricted (via RBAC) to only see and manage resources within its own namespace.
18. **Q: How can Python interact with 'Kube-Proxy'?**
    - **Answer**: Generally, you don't. Kube-Proxy is a low-level network component. Python interacts with the **API Server** to change the desired state of the network (e.g., Services).
19. **Q: What is the 'Finalizer' in a Kubernetes resource?**
    - **Answer**: A string that prevents the resource from being deleted until a specific action is taken (e.g., a Python script must clean up an S3 bucket before the K8s object is allowed to vanish).
20. **Q: How do you dry-run a K8s API call?**
    - **Answer**: By passing the `dry_run='All'` parameter to the API call. It verifies the logic without actually changing the state of the cluster.

---

[← Previous: SRE](18-python-sre.md) | [Next: CI/CD →](20-python-ci-cd.md)
