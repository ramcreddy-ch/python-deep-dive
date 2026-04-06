# 12. Python for Kubernetes — Production Deep Dive

> Wrapping `kubectl run` in Python's `subprocess` is an amateur pattern. Serious platform engineering against Kubernetes utilizes the official Kubernetes Python Client, communicates over HTTPS with the K8s API server using ServiceAccounts, and builds Custom Resource Controllers natively in Python.

---

## 🔍 The Kubernetes Python Client (`kubernetes`)

The official `kubernetes-client/python` library is a massively generated OpenAPI wrapper bridging Python to the Golang K8s API.

### Authentication & Config Loading
The client behaves differently on your laptop versus inside a Pod. Security best practices mandate using In-Cluster Config when deployed.

```python
from kubernetes import client, config
import os

def init_k8s():
    """Initializes K8s client regardless of environment"""
    if "KUBERNETES_SERVICE_HOST" in os.environ:
        # We are running INSIDE a pod.
        # Loads config from /var/run/secrets/kubernetes.io/serviceaccount/
        print("Loading In-Cluster Config")
        config.load_incluster_config()
    else:
        # We are running locally (DevOps laptop)
        # Loads config from ~/.kube/config
        print("Loading Local Kubeconfig")
        config.load_kube_config()

init_k8s()
v1 = client.CoreV1Api()
# List all pods in namespace
pods = v1.list_namespaced_pod(namespace="default")
for pod in pods.items:
    print(f"Pod: {pod.metadata.name} | Status: {pod.status.phase}")
```

---

## 🏭 Interacting with API Objects

The Python client requires passing deeply nested object definitions, which mirrors the standard YAML format exactly.

### Spawning a Batch Job for ML Training
When creating jobs programmatically, you don't write YAML—you instantiate classes.

```python
from kubernetes.client import V1Job, V1ObjectMeta, V1JobSpec, V1PodTemplateSpec, V1PodSpec, V1Container

def launch_training_job(job_name: str, image: str):
    batch_v1 = client.BatchV1Api()

    # Define Container
    container = V1Container(
        name="pytorch-worker",
        image=image,
        command=["python", "train.py", "--epochs=50"]
    )

    # Define Pod Spec
    template = V1PodTemplateSpec(
        metadata=V1ObjectMeta(labels={"app": "ml-training"}),
        spec=V1PodSpec(restart_policy="Never", containers=[container])
    )

    # Define Job Spec
    job_spec = V1JobSpec(
        template=template,
        backoff_limit=2 # Retry on failure
    )

    # Construct the final Job Object
    job = V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=V1ObjectMeta(name=job_name),
        spec=job_spec
    )

    # Dispatch to K8s API
    api_response = batch_v1.create_namespaced_job(
        body=job,
        namespace="ml-jobs"
    )
    print(f"Job launched. Status: {api_response.status}")
```

---

## 🧠 Building Operators in Python (Kopf)

Historically, Kubernetes Operators (Custom Controllers) were written exclusively in Go using Kubebuilder. Now, Python is an industry standard for MLOps operators thanks to the **Kopf (Kubernetes Operator Pythonic Framework)** library.

If you create a Custom Resource Definition (CRD) called `ModelDeployment`, Knopf lets you write Python functions that evaluate anytime one is created.

```python
# operator.py
import kopf
import kubernetes.client as k8s

@kopf.on.create('mlplatform.dev', 'v1', 'modeldeployments')
def create_fn(body, spec, name, namespace, logger, **kwargs):
    """
    Triggered instantly whenever a user applies a YAML file:
    kind: ModelDeployment
    name: fraud-detector
    """
    model_uri = spec.get('modelUri')
    replicas = spec.get('replicas', 1)
    
    logger.info(f"Received request to deploy model {name} from {model_uri}")
    
    # 1. We translate the custom CRD into a standard K8s Deployment dynamically
    apps_v1 = k8s.AppsV1Api()
    
    # ... Build V1Deployment object for vLLM or Triton Server based on model_uri ...
    
    # 2. Tell Kopf that the newly created raw Deployment is a "child" of our CRD
    # This ensures that if the user deletes the custom CRD, K8s auto-deletes the deployment
    kopf.adopt(deployment_obj)
    
    apps_v1.create_namespaced_deployment(namespace=namespace, body=deployment_obj)
    
    # Update the CRD status to show it worked
    return {'status': 'Successfully provisioned serving endpoints'}
```

---

## 🎯 Senior Engineer Interview Questions

**Q1: How does `config.load_incluster_config()` actually authenticate the Python application to the K8s API server?**
> **Answer:** Every pod in Kubernetes inherently has a ServiceAccount attached to it (either the `default` one, or one you specify). Kubelet automatically mounts the authentication token, the CA certificate, and the local namespace data as files on the container's disk at `/var/run/secrets/kubernetes.io/serviceaccount/`. The `load_incluster_config()` function simply reads that token string and injects it as a Bearer Token header into the Python HTTPS client used to query the API server at the IP address injected into the container's `KUBERNETES_SERVICE_HOST` env var.

**Q2: We use the Python client to `list_namespaced_pod()`. Our namespace has 50,000 pods. The Python script triggers an OOMKilled error. How do we fix this?**
> **Answer:** Standard API calls load the entire response JSON array into memory before coercing it to Python objects. Instead of one massive GET request, we use the Kubernetes API Pagination. We pass the `_continue` token and `limit` to the API request or, preferably, use the `kubernetes.watch` module to stream discrete events (Add/Update/Delete) over a persistent connection, processing the topology one item at a time.

**Q3: Explain the `kopf.adopt()` or "Owner References" mechanism in Kubernetes Python Operators.**
> **Answer:** Kubernetes has a built-in garbage collector. Without owner references, if your Python Custom Controller receives a `Model` CRD, spins up a Deployment, and later the user deletes the `Model` CRD, the Deployment is orphaned forever, costing money. Injecting an OwnerReference embeds a metadata link stating "This Deployment is Owned by This Custom Object". When K8s detects the deletion of the owner, the cascading garbage collector automatically prunes all child resources seamlessly, removing the need for us to write Python cleanup code.

---

[← Previous: Python for SRE](11-python-sre.md) | [Back to Index](../README.md) | [Next: Python for CI/CD →](13-python-cicd.md)
