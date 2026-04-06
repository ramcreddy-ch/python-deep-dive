# 11. Python for SRE & Observability — Production Deep Dive

> Site Reliability Engineering (SRE) is what happens when you ask a software engineer to design an operations team. Python is the dominant language for building "glue" systems—custom monitoring agents, auto-remediators, and log-parsing bots that bridge the gap between Datadog, Prometheus, Slack, and Kubernetes.

---

## 🔍 Structured Logging (The Absolute Rule)

If your application uses `print()`, it is not production-ready. 
Standard `logging` is slightly better, but modern log aggregators (ELK, Datadog/Splunk) expect **JSON Structured Logging**. 

If you log unstructured strings, an SRE has to write expensive, brittle Regex rules to parse metrics out of it. If you log JSON, it indexes automatically.

```python
import structlog
import logging

# Replaces standard library logging with pure, beautiful JSON
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer() # Output as JSON
    ]
)

log = structlog.get_logger()

# Do NOT do this:
# log.info(f"Payment {payment_id} processed by {user_id} taking {duration}ms")

# Do this: Every key becomes a graphable, filterable metric in Splunk/Datadog
log.info("payment_processed", payment_id="txn-9923", user_id="u-12", duration_ms=45)
```
*Output: `{"payment_id": "txn-9923", "user_id": "u-12", "duration_ms": 45, "event": "payment_processed", "level": "info", "timestamp": "2024-05-18T12:00:00Z"}`*

---

## 🏭 Exposing Prometheus Metrics

SREs require applications to expose white-box metrics. Python microservices usually do this via `/metrics` HTTP endpoints. 

```python
from prometheus_client import Counter, Histogram, start_http_server
import time
import random

# Metric Definitions
# Counters only ever go up (e.g., total requests)
REQ_COUNT = Counter('app_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])
# Histograms track distributions (P99 latency)
REQ_LATENCY = Histogram('app_request_latency_seconds', 'Request Latency', ['endpoint'])

def process_request():
    start = time.time()
    
    # Increment counter (labels matching the definition)
    REQ_COUNT.labels(method='POST', endpoint='/api/v1/ml/predict').inc()
    
    # Simulate work
    time.sleep(random.uniform(0.1, 0.5))
    
    # Record duration
    REQ_LATENCY.labels(endpoint='/api/v1/ml/predict').observe(time.time() - start)

if __name__ == '__main__':
    # Starts an HTTP server on port 8000. 
    # The Kubernetes Prometheus ServiceMonitor scrapes this port.
    start_http_server(8000)
    while True:
        process_request()
```

---

## 🔧 Building Custom Auto-Remediation (Incident Bots)

SREs seek to automate themselves out of a job. If an incident has a known runbook, a Python daemon should execute it securely before paging a human.

### The Webhook Receiver Pattern (FastAPI)
Using FastAPI to catch Alertmanager webhooks.

```python
from fastapi import FastAPI, Request
import subprocess
import structlog

app = FastAPI()
log = structlog.get_logger()

@app.post("/webhook/alertmanager")
async def handle_alert(request: Request):
    payload = await request.json()
    
    for alert in payload.get("alerts", []):
        alert_name = alert["labels"]["alertname"]
        
        # Mapping logic
        if alert_name == "HighMemoryUsage":
            pod_name = alert["labels"]["pod"]
            namespace = alert["labels"]["namespace"]
            log.warning("auto_remediation_triggered", action="restart_pod", pod=pod_name)
            
            # Subprocess wrapper to execute runbook
            # (In reality, use the python-kubernetes library)
            subprocess.run(["kubectl", "delete", "pod", pod_name, "-n", namespace])
            
    return {"status": "processed"}
```

---

## 🎯 Senior Engineer Interview Questions

**Q1: What is the primary difference between a Counter and a Gauge in Prometheus, and how would you implement them in Python?**
> **Answer:** A `Counter` is a monotonically increasing value—it only goes up (or resets to 0 on restart). You use it for things like "total requests" or "total errors". A `Gauge` can go up or down. You use it for snapshot values like "current active connections", "CPU utility", or "queue depth". In Python via `prometheus_client`, you invoke `counter.inc()` versus `gauge.set(value)`. 

**Q2: We need to instrument an existing bloated Flask API with Prometheus metrics to track latency across all 50 endpoints. Do we have to modify all 50 functions?**
> **Answer:** No. We should write a middleware or a decorator. In Flask/FastAPI, we write a single middleware function that intercepts every incoming request. It records the current time (`time.perf_counter()`), yields back down the stack (or awaits the response), calculates the duration, extracts the endpoint path from the request object, and records the metric (`Histogram.labels(endpoint=path).observe(duration)`).

**Q3: Describe how to build a Python health-check probe that prevents cascading failures in Kubernetes.**
> **Answer:** In K8s, we expose both a Liveness and Readiness probe endpoint. In our Python app, `/health/live` should simply `return 200 OK` (proving the thread is not deadlocked). Removing the pod if it's dead. However, `/health/ready` should actively test downward dependencies (e.g., attempt a fast `SELECT 1` on the DB connection pool). If the DB test fails, return `503 Service Unavailable`. K8s won't kill the pod, but it will instantly remove it from the Service load-balancer, preventing user traffic from routing to a pod that can't fulfill requests.

**Q4: Your Python application logs are filling up the host's `/var/log` partition. What standard tool do SREs use to manage this constraint?**
> **Answer:** If we are logging locally to disk instead of stdout, we must use Log Rotation. We can configure this at the infrastructure level via Linux `logrotate` service, or natively in Python using `logging.handlers.TimedRotatingFileHandler` or `RotatingFileHandler` (which automatically moves and compresses logs when they hit a certain size limit, deleting files older than X days).

---

[← Previous: Python for Cloud](10-python-cloud.md) | [Back to Index](../README.md) | [Next: Python for Kubernetes →](12-python-kubernetes.md)
