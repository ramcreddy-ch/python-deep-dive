# 18. Python for SRE & Observability — Logs, Metrics & Tracing

> "If it isn't monitored, it isn't in production. An expert doesn't just look at 'Uptime'; they look at 'Latencies', 'Error Budgets', and 'Distributed Traces' to find the root cause of a failure before the customer even notices it."

---

## ❓ The 'Why' (High-Level)
Site Reliability Engineering (SRE) is the practice of applying software engineering to operations. In a massive cloud system, you can't "tail" a log file on one server. You need **Observability**—the ability to understand the internal state of a system just by looking at its outputs. Python is the "Glue" of observability, providing the tools to generate, collect, and analyze the "Three Pillars": **Logs**, **Metrics**, and **Traces**.

---

## 🌱 Module 1: The Basics (Junior) — Logging
Logging is the first step. It tells you **what happened**.

### 1. The `logging` Module
Never use `print()` for production diagnostics. Use the `logging` module.
```python
import logging
# Basic Setup
logging.basicConfig(level=logging.INFO)
logging.info("System started successfully")
logging.error("Database connection failed!")
```

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — Structured Data
Mid-level engineers don't log "Sentences"; they log **Data**.

### 1. Structured Logging (JSON)
Modern log aggregators (ELK, Datadog) prefer JSON because they can index the fields for fast searching.
- **Why?**: Searching for `user_id:123` in a database is 1,000x faster than scanning raw text files.

### 2. Log Rotation
You can't let one log file grow to 100GB and fill up your server's disk.
- **Solution**: Use `RotatingFileHandler` to automatically split and delete old logs.

---

## 🌳 Module 3: Advanced Mechanics (Senior) — Metrics & Traces
Senior engineers look at the "Health" of the whole system using numbers.

### 1. Prometheus Metrics
Metrics tell you **how the system is performing** over time.
```python
from prometheus_client import start_http_server, Counter

# A Counter only ever goes UP (e.g., total requests)
REQUESTS = Counter('http_requests_total', 'Total HTTP Requests')

def process_request():
    REQUESTS.inc()  # Increment the counter
```

### 2. Distributed Tracing (OpenTelemetry)
If User -> Service A -> Service B -> Database, how do you know which step was slow?
- **Traces**: Attach a unique **Correlation ID** to the request header so you can see the entire journey across 10 different servers in one timeline.

---

## 🔥 Module 4: Principal Architect (Principal) — Resilience & SLOs
At the highest level, you define what "Reliable" actually means.

### 1. SLOs & Error Budgets
- **SLO (Service Level Objective)**: "99.9% of requests must finish under 200ms."
- **Error Budget**: The 0.1% of "Allowable Failure." If you use up your budget, a principal engineer stops all new feature work to focus on stability.

### 2. Auto-Remediation (Self-Healing)
A principal engineer writes Python "Agents" that watch the metrics. If memory hits 90%, the agent automatically captures a memory dump and restarts the service, waking up the developer only if the restart fails.

---

## 🏗️ Case Study: The Midnight Outage Prevention
A social network saw a sudden 10% spike in error rates at 2 AM.
- **The Junior Approach**: Scanned raw log files on 100 servers. (Took 3 hours to find nothing).
- **The Principal Approach**: Used **Prometheus** to see that the error spike correlated exactly with a database "Lock Contention" metric and used **OpenTelemetry** to find the specific "slow query" causing it.
- **Result**: The root cause was identified and a fix deployed in **20 minutes**, preventing a total system crash.

---

## ⚡ Anti-Patterns & Expert Traps

### 1. Logging PII (Sensitive Data)
**NEVER** log passwords, credit card numbers, or personally identifiable information (PII). It's a massive security risk and a violation of laws like GDPR.

### 2. High-Cardinality Metrics
Don't put a `user_id` inside a Prometheus metric name. It will create millions of separate time-series on your monitoring server and crash it. **Expert fix**: Use "Aggregation" to count groups of users instead.

---

## 🎯 Top 20 Principal Interview Questions (SRE & Observability)

1. **Q: What are the 'Three Pillars of Observability'?**
   - **Answer**: 1. **Logs** (Immutable records of discrete events). 2. **Metrics** (Aggregated numerical data over time). 3. **Traces** (The end-to-end journey of a single request across multiple services).
2. **Q: Why avoid `print()` in production code?**
   - **Answer**: it can't be easily turned off, it doesn't support log levels (like ERROR vs DEBUG), and it doesn't provide metadata like timestamps or line numbers automatically.
3. **Q: Explain 'Structured Logging'.**
   - **Answer**: Writing logs in a machine-readable format (like JSON) so that monitoring tools can easily index, search, and graph specific fields without manual parsing.
4. **Q: What is 'Prometheus' and how does it collect data?**
   - **Answer**: An open-source monitoring system that **Pulls** (scrapes) numerical metrics from your application over HTTP. It's essentially a high-performance "Time-Series Database."
5. **Q: What is a 'Correlation ID' in distributed tracing?**
   - **Answer**: A unique ID generated at the start of a request and passed in headers to every downstream service. This allows all logs from all servers for that specific request to be linked together.
6. **Q: Explain 'SLI', 'SLO', and 'SLA'.**
   - **Answer**: **SLI** (Indicator): What you measure (e.g., latency). **SLO** (Objective): Your target (e.g., <500ms). **SLA** (Agreement): The legal contract with customers (e.g., "We pay you if it's down more than 1 hour").
7. **Q: What is 'Log Rotation'?**
   - **Answer**: The process of closing the current log file, renaming it (e.g., `app.log.1`), and starting a new one once it reaches a certain size, preventing disk space exhaustion.
8. **Q: What is a 'Health Check' endpoint?**
   - **Answer**: A URL (usually `/health` or `/ready`) that returns a `200 OK` if the app is healthy, allowing load balancers and Kubernetes to know when to send traffic or restart a pod.
9. **Q: Explain 'Sentry' or 'Rollbar' for error tracking.**
   - **Answer**: Tools that capture **Uncaught Exceptions** in real-time, grouping them by type and providing a full variable state at the time of the crash.
10. **Q: What is 'OpenTelemetry' (OTEL)?**
    - **Answer**: A vendor-neutral standard for generating and exporting logs, metrics, and traces, allowing you to switch monitoring providers (like Datadog to New Relic) without changing your code.
11. **Q: Why is 'High-Cardinality' bad in Prometheus?**
    - **Answer**: Cardinality is the number of unique combinations of labels. If you use a `user_id` as a label, you create a new time-series for every user, which will eventually crash the Prometheus server's memory.
12. **Q: What is 'Canary Deployment'?**
    - **Answer**: Releasing a new version of code to a tiny percentage (e.g., 1%) of users first and monitoring its error rates before rolling it out to everyone.
13. **Q: Explain 'Circuit Breaker' in an SRE context.**
    - **Answer**: A safety mechanism that stops a service from calling a failing downstream dependency. This avoids "Cascading Failures" where one slow service brings down the entire platform.
14. **Q: How can you log a full Traceback in an `except` block?**
    - **Answer**: By using `logging.exception("message")`. This automatically captures the traceback from `sys.exc_info()` and adds it to the log entry.
15. **Q: What is 'Rate Limiting'?**
    - **Answer**: Controlling the number of requests a user can make to an API to prevent abuse and ensure the system remains stable for everyone else.
16. **Q: What is 'Distributed Tracing Span'?**
    - **Answer**: A single "Unit of Work" in a trace (e.g., a database query or a function execution). A trace is a collection of these spans.
17. **Q: How does a 'Gauge' metric differ from a 'Counter'?**
    - **Answer**: A **Counter** only goes UP (e.g., total visits). A **Gauge** can go up or down (e.g., current CPU usage or current number of users logged in).
18. **Q: What is 'Alert Fatigue' and how do you prevent it?**
    - **Answer**: When developers are overwhelmed by too many non-critical alerts. Prevent it by only alerting on **Actionable** issues and tuning thresholds based on SLOs.
19. **Q: What is 'Runbook-as-Code'?**
    - **Answer**: Automated Python scripts that perform the steps an SRE would normally do manually to fix an incident (e.g., "Clear cache and restart").
20. **Q: How do you implement a 'Graceful Shutdown' in SRE?**
    - **Answer**: By catching signals (`SIGTERM`), stopping the acceptance of new requests, finishing current tasks, and closing database connections before exiting.

---

[Previous: Cloud & Boto3](17-python-cloud-boto3.md) | [Next: Kubernetes Operators →](19-python-kubernetes.md)
