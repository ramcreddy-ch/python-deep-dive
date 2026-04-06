# 14. Networking & HTTP — Production Deep Dive

> "It works on my machine" usually means "My machine has 1ms latency to the DB and no firewall." In production, networks are hostile. Packets drop, DNS fails, and APIs throttle. Building robust HTTP clients and high-throughput servers in Python requires more than just `requests.get()`.

---

## 🔍 Modern HTTP Clients

### The Problem with `requests`
`requests` is synchronous and block-based. It is perfect for scripts, but terrible for high-throughput microservices. Every open `requests` call holds a dedicated thread hostage.

```python
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Production Pattern: NEVER use raw requests.get()
# Always establish a persistent session with connection pooling and retries
def create_robust_session():
    session = requests.Session()
    
    # Retry 3 times on 500, 502, 503, 504 with exponential backoff
    retries = Retry(total=3, backoff_factor=0.3, status_forcelist=[ 500, 502, 503, 504 ])
    
    # Mount adapter allowing 100 persistent connections in the pool
    adapter = HTTPAdapter(max_retries=retries, pool_connections=100, pool_maxsize=100)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    return session

http = create_robust_session()
# Crucial: Always set timeouts. Without this, a dead server hangs your thread infinitely.
resp = http.get("https://api.github.com", timeout=(3.0, 10.0)) # (connect, read)
```

### The Async Standard: `httpx`
When you need to make 500 API calls concurrently (e.g., verifying links or hitting an LLM endpoint), `httpx` integrates cleanly with `asyncio`.

```python
import asyncio
import httpx

async def fetch_urls(urls):
    # httpx.AsyncClient handles persistent connection pooling asynchronously
    async with httpx.AsyncClient(http2=True) as client:
        tasks = [client.get(url, timeout=5.0) for url in urls]
        # Executes all requests simultaneously
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        return responses
```

---

## 🏭 API Development (FastAPI)

FastAPI replaced Flask as the industry standard because it relies on Pydantic (data validation) and Starlette (ASGI async capability), making it strongly typed and insanely fast.

### Dependency Injection & Security
Platform APIs need to securely validate tokens without duplicating code in every endpoint.

```python
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel

app = FastAPI()

# 1. Shared Dependency checks auth once
async def verify_auth_token(x_api_token: str = Header(...)):
    if x_api_token != "super-secret-token":
        raise HTTPException(status_code=401, detail="X-API-Token invalid")
    return "user_id_123"

# 2. Strict Input/Output Schema mapping
class PromptRequest(BaseModel):
    query: str
    max_tokens: int = 100

class PromptResponse(BaseModel):
    answer: str
    compute_time_ms: int

# 3. Secure, typed endpoint
@app.post("/v1/llm/generate", response_model=PromptResponse)
async def generate_text(
    payload: PromptRequest, 
    user_id: str = Depends(verify_auth_token) # Injected automatically!
):
    # Pydantic guarantees payload.max_tokens is an integer
    result = await call_heavy_model(payload.query, payload.max_tokens)
    return {"answer": result, "compute_time_ms": 150}
```

---

## 🔧 Networking Fundamentals in Python

### Sockets and DNS
Sometimes you just need to check if a port is open before allowing a CI pipeline to proceed, or force a DNS resolution cache clear.

```python
import socket

def wait_for_port(host: str, port: int, timeout: int = 5) -> bool:
    """SRE tool: check if a raw TCP port is accepting connections"""
    # AF_INET = IPv4, SOCK_STREAM = TCP
    with socket.socket(socket.AF_INET, socket.socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            # Returns 0 on success (connected!)
            result = s.connect_ex((host, port))
            return result == 0
        except socket.gaierror:
            # DNS resolution failed
            return False
            
print(wait_for_port("google.com", 443)) # True
print(wait_for_port("localhost", 9999)) # False
```

---

## 🎯 Senior Engineer Interview Questions

**Q1: What is the difference between WSGI (Gunicorn/Flask) and ASGI (Uvicorn/FastAPI)?**
> **Answer:** WSGI (Web Server Gateway Interface) is strictly synchronous. It processes one request per worker thread/process from start to finish. If the request blocks for a 5-second DB query, that worker is paralyzed. ASGI (Asynchronous Server Gateway Interface) supports `async/await`. While the DB query is executing over the network, the worker pauses the coroutine and actively serves thousands of other incoming HTTP requests, yielding massively higher throughput for I/O bound APIs.

**Q2: We deployed a Python service to Kubernetes, and it's making external HTTP requests to a 3rd party API. Periodically, we get `ConnectionResetError` or `Timeout`. What is happening at the TCP level?**
> **Answer:** This is a classic Connection Pooling edge case. `requests.Session()` keeps TCP connections open (Keep-Alive). If the 3rd party API endpoint (or an intermediate load balancer/NAT gateway) silently tears down idle connections via an idle timeout (e.g., 60 seconds), but the Python client still thinks the connection is alive in its pool, Python will attempt to send data down a closed socket. The fix is to ensure the Python client's connection pool `keep_alive` timeout is explicitly set *lower* than the upstream load balancer's timeout.

**Q3: Describe the mechanics of a Server-Sent Events (SSE) endpoint in FastAPI and why it's preferred over WebSockets for LLM text generation.**
> **Answer:** SSE is a unidirectional channel where the client initiates a standard HTTP GET, but the server keeps the connection open, streaming text payloads chunks as they are generated (e.g., `yield f"data: {token}\n\n"` in Python). Unlike WebSockets, it operates over standard HTTP, making it immune to strict proxy/firewall websocket drops, and it relies on standard HTTP load balancing logic. It's ideal for LLM generation because data only flows Server -> Client.

**Q4: In Python, `socket.gethostbyname("api.service.local")` is returning a stale IP address after a Kubernetes pod restart. Why, and how do we resolve it?**
> **Answer:** Python's `socket` library delegates DNS resolution entirely to the underlying OS (`libc` `getaddrinfo` on Linux). If the OS has cached the DNS lookup (e.g., via `nscd` or `systemd-resolved`), Python will return the stale IP. More nefariously, long-living HTTP connection pools (`requests.Session()`) resolve DNS *once* upon establishing the connection, and never look up the DNS again. If the upstream Pod rotates IP addresses, the session pool is poisoned. We resolve this by enforcing a max-lifespan on connections within the pool so they gracefully close and trigger a fresh DNS/TCP handshake.

---

[← Previous: Python for CI/CD](13-python-cicd.md) | [Back to Index](../README.md) | [Next: Data Engineering →](15-data-engineering.md)
