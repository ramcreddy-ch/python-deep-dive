# 15. Networking & HTTP — Requests, FastAPI & APIs

> "Networking is the 'Connecting Tissue' of our digital world. An expert doesn't just 'call an API'; they understand how to handle timeouts, retries, and high-performance async serving with FastAPI and Pydantic validation."

---

## 🌱 The Basics: Making HTTP Requests
The entry-level way to "talk" to the internet using the **`requests`** library.

```python
import requests

# 1. Simple GET
response = requests.get("https://api.github.com/users/ramcreddy-ch")

# 2. Check status and output
if response.status_code == 200:
    print(response.json())
```

---

## 🌿 Intermediate: FastAPI & Pydantic
`FastAPI` is the modern standard for building Python APIs. It's built on **AsyncIO** and uses **Pydantic** for ultra-fast data validation.

**Real Use (Platform/Microservice)**:
A production API that validates input automatically.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str

@app.post("/users")
async def create_user(user: User):
    return {"message": f"User {user.name} created!"}
```

---

## 🌳 Advanced: Authentication & Middleware
Senior engineers add security layers to their APIs. 

- **JWT (JSON Web Token)**: used for stateless authentication.
- **Middleware**: Code that runs **before** and **after** every request (e.g., for logging or CORS).

```python
# Expert Pattern: Middleware. 
# 1. Intercepts incoming request.
# 2. Checks for a specific header.
# 3. Rejects if missing.
```

---

## 🔥 Expert: Performance (HTTP/2 & keep-alive)
Principal engineers optimize "Under the Hood."

### 1. Connection Pooling
Instead of creating a new connection for every request, they use a **Session** to "Keep-Alive" the connection, saving the overhead of the TLS handshake.

### 2. Async Client (httpx)
For high-scale automation, use **`httpx`** instead of `requests` to make 1,000 non-blocking API calls simultaneously.

---

## 🎯 Top 20 Principal Interview Questions (Networking & HTTP)

1. **Q: What is the difference between `Requests` and `httpx`?**
   - **Answer**: `Requests` is synchronous and blocking. `httpx` is a modern successor that supports both synchronous and **Asynchronous** (non-blocking) requests, as well as HTTP/2.
2. **Q: Why is 'Pydantic' used in FastAPI?**
   - **Answer**: It is used for **Data Serialization** and **Validation**. It automatically converts incoming JSON into Python objects while checking types (e.g., ensuring an ID is an integer).
3. **Q: What is a 'RESTful API'?**
   - **Answer**: An architectural style for software that uses standard HTTP methods (GET, POST, PUT, DELETE) to manage "Resources" (like Users or Orders). 
4. **Q: Explain 'JWT Authentication'.**
   - **Answer**: It is a stateless "Voucher" (token) that contains user data. The server signs it, and the client sends it in the `Authorization` header on every request. The server verifies the signature without needing to check a database.
5. **Q: What is 'Middleware' in a web framework?**
   - **Answer**: It is a "Hook" that allows you to execute code **before** the request reaches the handler and **after** the response is generated (e.g., for logging, authentication, or CORS headers).
6. **Q: What is 'CORS' and how do you handle it in FastAPI?**
   - **Answer**: **Cross-Origin Resource Sharing**. It's a browser security feature that denies requests from different domains. In FastAPI, you use the `CORSMiddleware` to whitelist specific origins.
7. **Q: What is the purpose of 'HTTP Status Codes'? Name some important ones.**
   - **Answer**: They indicate the outcome of the request. **200** (OK), **201** (Created), **400** (Bad Request), **401** (Unauthorized), **403** (Forbidden), **404** (Not Found), **500** (Server Error).
8. **Q: How do you handle 'Timeouts' in a production API call?**
   - **Answer**: **Never** make an API call without a timeout. In `requests`, use `requests.get(url, timeout=5)`. This prevents your whole application from hanging if the external service is slow.
9. **Q: What is 'Idempotency' in HTTP methods?**
   - **Answer**: An operation is idempotent if doing it multiple times has the same result as doing it once. **GET, PUT, and DELETE** are idempotent. **POST** is generally NOT (e.g., creating a user twice creates 2 users).
10. **Q: What is 'Connection Pooling'?**
    - **Answer**: The practice of keeping a set of database or network connections open to be reused for future requests, rather than opening and closing a new connection every single time.
11. **Q: Explain 'Starlette' and its relation to FastAPI.**
    - **Answer**: Starlette is the high-performance **ASGI framework** that FastAPI is built on. It handles the low-level logic of HTTP and WebSocket routing.
12. **Q: What is the difference between `@app.get()` and `@app.post()`?**
    - **Answer**: `GET` is for **Retrieving** data. `POST` is for **Creating/Sending** data to be processed.
13. **Q: How do you handle 'Rate Limiting' in Python?**
    - **Answer**: Using a library like `slowapi` or by implementing a "Token Bucket" algorithm with a backend like **Redis** to track user request counts.
14. **Q: What is an 'ASGI' vs 'WSGI' server?**
    - **Answer**: **WSGI** (like Gunicorn) is synchronous. **ASGI** (like Uvicorn) supports **AsyncIO**, allowing it to handle many concurrent connections on a single thread.
15. **Q: What is the purpose of the `User-Agent` header?**
    - **Answer**: It identifies the client software (e.g., "Chrome" or "Python-Requests") making the request. Some APIs block generic Python crawlers and require a custom User-Agent.
16. **Q: How do you securely pass an 'API Key' in a request?**
    - **Answer**: **Never** put keys in the URL. Always send them in the **HTTP Headers** (e.g., `X-API-Key` or `Authorization: Bearer <token>`).
17. **Q: What is 'JSONP' and why is it no longer used?**
    - **Answer**: An old hack to bypass CORS. It's insecure because it executes script tags from other domains. It has been replaced by the official CORS standard.
18. **Q: Explain 'WebSocket' and how it differs from HTTP.**
    - **Answer**: HTTP is "Request-Response." WebSocket is **Bi-directional and Persistent**. Once connected, both the server and client can send messages at any time without a new request.
19. **Q: What is the purpose of the `Content-Type` header?**
    - **Answer**: It tells the server (and client) how to interpret the data body (e.g., `application/json`, `text/html`, or `multipart/form-data`).
20. **Q: How do you perform 'Bulk' operations in a REST API?**
    - **Answer**: Usually by sending a **List of Objects** in a single `POST` or `PATCH` request to a specific "bulk" endpoint (e.g., `/users/bulk-update`).

---

[← Previous: Testing](../Level-2/14-testing-mocking.md) | [Next: DevOps →](16-python-devops.md)
