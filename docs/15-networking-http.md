# 15. Networking & HTTP/2 — Sockets, Requests & Binary Protocols

> "The network is always unreliable. An expert doesn't assume a packet will arrive; they design for 'Partial Failures', 'Network Partitions', and 'Late Arrival'. Mastering networking is about understanding how raw bytes move across the wire through the 7-layer OSI model."

---

## ❓ The 'Why' (High-Level)
In a cloud-native world, no application is an island. Everything is a **Distributed System**. Your Python microservice talks to a database, an AWS S3 bucket, and a third-party payment API. A principal engineer knows that the "Speed of Light" is a real constraint, and that choosing between **TCP** (Reliable) and **UDP** (Fast) can be the difference between a high-performance gaming server and a slow, buggy website.

---

## 🌱 Module 1: The Basics (Junior) — The HTTP Cycle
Most Python networking happens over HTTP (HyperText Transfer Protocol).

### 1. The Request-Response Cycle
1.  **Request**: You ask for data (GET, POST, PUT, DELETE).
2.  **Status Codes**: The server replies with a code:
    - **200**: OK (Everything worked).
    - **404**: Not Found (Wrong URL).
    - **500**: Internal Server Error (The server crashed).

### 2. Basic Sockets
A Socket is one end of a two-way communication link between two programs running on the network.
```python
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP Socket
s.connect(("google.com", 80))
```

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — The `requests` Library
Junior engineers use `urllib`; professionals use **`requests`** or **`httpx`**.

### 1. Making API Calls
```python
import requests

response = requests.get("https://api.github.com/user", auth=('user', 'pass'))
if response.status_code == 200:
    data = response.json()  # Automatically parses the JSON body!
```

### 2. Timeouts & Sessions
Always use a `Session` object to reuse the same TCP connection for multiple requests, making your code 2x-3x faster.
```python
session = requests.Session()
session.get("https://api.com/v1")
session.get("https://api.com/v2")  # Reuses the same connection!
```

---

## 🌳 Module 3: Advanced Mechanics (Senior) — HTTP/2 & WebSockets
Senior engineers look for performance beyond the standard "Request/Response" model.

### 1. HTTP/2 and Multiplexing
Standard HTTP 1.1 can only handle one request at a time per connection. **HTTP/2** allows you to send **multiple requests simultaneously** over a single socket (Multiplexing).
- **Expert tool**: Use **`httpx`** instead of `requests` for native HTTP/2 support.

### 2. WebSockets for Real-time Data
If you need a "Push" from the server (like a chat app or a stock ticker), use **WebSockets**. Unlike HTTP, the connection stays open forever.

---

## 🔥 Module 4: Principal Architect (Principal) — gRPC & Protobuf
At the highest level, you move away from human-readable JSON to **Binary Protocols**.

### 1. gRPC (Google Remote Procedure Call)
gRPC uses **Protocol Buffers (Protobuf)** to serialize data into binary. It's 10x smaller and faster than JSON.
- **Why?**: In a system with 1,000 microservices, the "Network Cost" of parsing JSON becomes a major bottleneck. gRPC solves this.

### 2. Service Discovery & Idempotency
- **Idempotency**: Ensuring that if a request is sent twice (due to a retry), it only happens **once** in the database. 
- **Service Discovery**: How does Service A find the IP address of Service B in a cluster of 10,000 nodes? (Consul, Etcd, or K8s DNS).

---

## 🏗️ Case Study: Building a High-Performance API Gateway
A streaming company was struggling with slow mobile app load times. The app was making **50 separate HTTP calls** to get user data, movie lists, and recommendations.
- **The Junior Approach**: Add more threads to handle the requests. (Didn't help; the bottleneck was the mobile network).
- **The Principal Approach**: Built an **API Gateway** in Python that combined those 50 requests into **1 single HTTP/2 call** using gRPC on the backend.
- **Result**: Mobile app load times dropped by **70%**, and user retention increased by 15%.

---

## ⚡ Anti-Patterns & Expert Traps

### 1. Hardcoding IP Addresses
Never hardcode `192.168.1.50` in your code. Use **Environmental Variables** or **DNS Names** (`db-service.prod.svc`).

### 2. Ignoring Timeouts
If you don't set a timeout, your Python script might "Hang" forever if a server is down, eventually using up all your system resources. **Always** set `timeout=5`.

---

## 🎯 Top 20 Principal Interview Questions (Networking & HTTP/2)

1. **Q: What is the OSI Model and why is it important?**
   - **Answer**: It's a 7-layer framework representing how data moves through a network. As a Python developer, you mostly work at **Layer 7 (Application - HTTP)**, but you must understand **Layer 4 (Transport - TCP/UDP)** for performance.
2. **Q: Explain the difference between TCP and UDP.**
   - **Answer**: **TCP** is reliable (retries if data is lost, keeps order). **UDP** is fast but "fire and forget" (used for video streaming and gaming where losing a single packet isn't critical).
3. **Q: How does HTTP/2 improve performance over HTTP/1.1?**
   - **Answer**: Through **Multiplexing** (sending multiple requests over one connection), **Header Compression** (HPACK), and **Server Push**.
4. **Q: What is a 'Three-Way Handshake' in TCP?**
   - **Answer**: The process of establishing a connection: **SYN** (Synchronize), **SYN-ACK** (Synchronize-Acknowledge), and **ACK** (Acknowledge).
5. **Q: What are REST APIs and what are their constraints?**
   - **Answer**: **REpresentational State Transfer**. Constraints include being **Stateless**, having a **Uniform Interface**, and being **Cacheable**.
6. **Q: What is the purpose of 'Keep-Alive' headers?**
   - **Answer**: To tell the server not to close the TCP connection immediately after the response, so it can be reused for the next request, saving the time of a new handshake.
7. **Q: Explain 'CORS' (Cross-Origin Resource Sharing).**
   - **Answer**: A security feature in browsers that prevents a website on one domain from making requests to another domain unless specifically allowed by the server.
8. **Q: What is 'JSONP' (and why is it obsolete)?**
   - **Answer**: A historical hack to bypass CORS. It's obsolete because it had major security risks and was replaced by the official CORS standard.
9. **Q: Explain 'gRPC' and 'Protocol Buffers'.**
   - **Answer**: gRPC is a high-performance RPC framework. Protocol Buffers is the **Binary Serialization** format it uses, which is much faster and more compact than JSON.
10. **Q: What is a 'WebSocket'?**
    - **Answer**: A protocol providing **Full-Duplex** (two-way) communication over a single TCP connection, allowing the server to push data to the client instantly.
11. **Q: How do you handle 'Retries' correctly?**
    - **Answer**: Using **Exponential Backoff** (waiting longer between each try) and **Jitter** (adding a bit of randomness to prevent a "thundering herd" effect on the server).
12. **Q: What is 'Idempotency' in APIs?**
    - **Answer**: The property where multiple identical requests have the same effect as a single request (e.g., `PUT` is idempotent, `POST` is usually not).
13. **Q: Explain 'TLS/SSL' Handshakes.**
    - **Answer**: The process where a client and server negotiate encryption keys and verify certificates before any data is sent.
14. **Q: What is a 'Reverse Proxy' (e.g., Nginx)?**
    - **Answer**: A server that sits in front of your Python app, handling SSL termination, load balancing, and static file serving.
15. **Q: What is 'DNS Propagation'?**
    - **Answer**: The time it takes for a change in a domain's IP address to be updated across all internet servers worldwide.
16. **Q: What is the difference between `PUT` and `PATCH`?**
    - **Answer**: `PUT` replaces the **Entire Resource**. `PATCH` performs a **Partial Update** to specific fields.
17. **Q: Explain 'Circuit Breaker' pattern in networking.**
    - **Answer**: If a service is failing repeatedly, the circuit breaker "Trips" and stops all requests to that service for a while to allow it to recover without being overwhelmed.
18. **Q: What is the `httpx` library and why should you use it?**
    - **Answer**: It is a next-generation HTTP client for Python that supports both sync and **async** calls and has native support for **HTTP/2**.
19. **Q: What is 'Service Discovery'?**
    - **Answer**: A system (like Kubernetes DNS or Consul) that automatically tracks the current IP addresses of all instances of a service as they scale up or down.
20. **Q: How can you inspect raw network packets in Python?**
    - **Answer**: By using low-level **Raw Sockets** or libraries like **Scapy** which can craft and sniff individual packets.

---

[Previous: Testing](14-testing-mocking.md) | [Next: Python for DevOps →](16-python-devops.md)
