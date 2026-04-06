# 18. Python for SRE & Observability — Monitoring, Logging & Tracing

> "Hope is not a strategy. Expert Site Reliability Engineers (SREs) use Python to build 'Eyes' for their infrastructure — measuring SLIs, auto-remediating failures, and ensuring that every error is caught, logged, and analyzed before it becomes an outage."

---

## 🌱 The Basics: Structured Logging
Entry-level logging is just `print()`. Professional logging uses a **Logger** that outputs **JSON**.

**Why?** JSON logs can be easily parsed by tools like **ELK (Elasticsearch/Logstash/Kibana)** or **Splunk**.

```python
import logging
import json

# 1. Custom Log Formatter for JSON
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "timestamp": self.formatTime(record)
        }
        return json.dumps(log_record)

# 2. Setup the logger
logger = logging.getLogger("SRE-App")
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# logger.info("Server started successfully")
```

---

## 🌿 Intermediate: Metrics (Prometheus)
`Prometheus` is the industry standard for monitoring. In Python, we use the **`prometheus_client`** to expose a `/metrics` HTTP endpoint that Prometheus "Scrapes" every few seconds.

- **Counter**: A number that only goes UP (e.g., Total Requests).
- **Gauge**: A number that goes UP and DOWN (e.g., Current RAM usage).

```python
from prometheus_client import start_http_server, Counter, Gauge
import random
import time

# Define metrics
REQUESTS = Counter("http_requests_total", "Total HTTP Requests")
CPU_USAGE = Gauge("system_cpu_usage", "Current CPU Usage Percentage")

# start_http_server(8000) # Expose at http://localhost:8000/metrics
```

---

## 🌳 Advanced: Distributed Tracing (OpenTelemetry)
Tracing allows you to follow a single request as it travels through 10 different microservices.

**Real Use (Platform/SRE)**:
Finding exactly which service in a chain is causing a 5-second delay.

```python
# Expert Pattern: OpenTelemetry. 
# 1. Decorate your function.
# 2. Python automatically generates a 'Span ID'.
# 3. Span is sent to a central server like Jaeger.
```

---

## 🔥 Expert: Auto-Remediation (Self-Healing)
Principal engineers don't just "Watch" the dashboard; they write Python scripts that **fix** the problems.

**Real Use (Cloud/K8s)**:
If a service's error rate is > 5%, the Python script automatically rolls back the latest deployment or restarts the POD.

---

## 🎯 Top 20 Principal Interview Questions (SRE & Observability)

1. **Q: What is the 'Three Pillars of Observability'?**
   - **Answer**: **Logs** (Events), **Metrics** (Aggregated data), and **Traces** (Request journeys).
2. **Q: Why is 'Structured Logging' (JSON) better than 'Plain Text'?**
   - **Answer**: Because it is **Machine-Readable**. You can query JSON logs in Elasticsearch to find "All 500 errors for User X in the last 5 minutes" instantly.
3. **Q: What is the difference between a 'Counter' and a 'Gauge' in Prometheus?**
   - **Answer**: A **Counter** only increases (like Total Requests). A **Gauge** can go up or down (like RAM usage).
4. **Q: Explain 'Service Level Objectives' (SLOs) and 'Error Budgets'.**
   - **Answer**: An **SLO** is a target (e.g., 99.9% uptime). An **Error Budget** is the amount of downtime you are allowed (e.g., 43 minutes per month). If you exceed the budget, you stop deploying new features.
5. **Q: How does the Python `logging` module handle different 'Log Levels'?**
   - **Answer**: **DEBUG** (low-level info), **INFO** (general events), **WARNING** (something unusual), **ERROR** (failure occurred), **CRITICAL** (app might crash).
6. **Q: What is 'Instrumenting' a core application?**
   - **Answer**: adding code (like Prometheus metrics or OpenTelemetry spans) to a production function so that its performance can be monitored externally.
7. **Q: What is 'Tracing' and why is it needed for microservices?**
   - **Answer**: It tracks a single request ID across multiple network calls to different servers. Without it, you can't tell which service in a stack of 10 is actually slow.
8. **Q: How do you avoid 'Log Bloat' in production?**
   - **Answer**: Setting the log level to **INFO** or **WARNING**, and only using **DEBUG** when actively troubleshooting an issue.
9. **Q: What is an 'Alerting Rule' in Prometheus?**
   - **Answer**: A query that triggers an alert (to Slack or PagerDuty) if a metric crosses a threshold (e.g., `requests_failed > 10%`).
10. **Q: What is 'Auto-Remediation'?**
    - **Answer**: A Python script that automatically acts when an alert is triggered (e.g., Automatically restarting a frozen worker process).
11. **Q: How do you handle 'Contextual Info' in logs for better debugging?**
    - **Answer**: Adding meta-data to every log line, such as `user_id`, `request_id`, and `server_name`.
12. **Q: What is the `logging.handlers.RotatingFileHandler`?**
    - **Answer**: A handler that automatically creates a new log file when the current one reaches a certain size, preventing the disk from filling up.
13. **Q: What is 'Distributed Tracing'?**
    - **Answer**: The ability to reconstruct the journey of a single user request across many independent services, even if they are written in different languages.
14. **Q: Explain 'Golden Signals' for monitoring.**
    - **Answer**: **Latency** (time), **Traffic** (demand), **Errors** (rate), and **Saturation** (resource use).
15. **Q: What is 'Synthetic Monitoring'?**
    - **Answer**: A Python script that acts like a real user, "Smoking" the website every minute to make sure it's working before a real user finds a bug.
16. **Q: How do you monitor 'Cold Starts' in an AWS Lambda?**
    - **Answer**: By logging and measuring the time between the function's first line of code and its final execution.
17. **Q: What is 'Cardinality' in Prometheus?**
    - **Answer**: The total number of unique label combinations. High cardinality (e.g., adding a `user_id` label to a metric) can crash your Prometheus server.
18. **Q: What is 'Centralized Logging'?**
    - **Answer**: Sending every log from every server/container to one central database (like ELK) so you can search them in one place.
19. **Q: What is the benefit of 'Asynchronous Logging'?**
    - **Answer**: It sends logs to a background thread so that the main application doesn't slow down while waiting for the disk/network to write a log line.
20. **Q: How do you test your 'Observability' tools?**
    - **Answer**: Using **Chaos Engineering** — intentionally breaking a service and making sure your dashboards and alerts detect it accurately.

---

[← Previous: Cloud](17-python-cloud.md) | [Next: Kubernetes →](19-python-kubernetes.md)
