# 28. Database Engineering — SQLAlchemy, Connection Pooling & Redis

> "Application servers are stateless; Databases are where the 'Truth' lives. An expert knows that slow SQL queries are the #1 cause of production outages, and mastering Object-Relational Mappers (ORMs) like SQLAlchemy is essential for building fast, secure, and maintainable data layers."

---

## 🌱 The Basics: SQLite & Basic Queries
The entry-level way to use a database in Python is via the built-in **`sqlite3`** module.

```python
import sqlite3

# 1. Connect to an in-memory database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# 2. Basic SQL
cursor.execute("CREATE TABLE users (id int, name text)")
cursor.execute("INSERT INTO users VALUES (1, 'Ram')")
# res = cursor.execute("SELECT * FROM users").fetchone()
```

---

## 🌿 Intermediate: SQLAlchemy (The ORM Standard)
`SQLAlchemy` is the standard for senior engineers. It maps a Python **Class** to an SQL **Table**.

**Real Use (API/Platform)**:
A Model that defines your database schema in a clean, version-controlled way.

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DBUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
```

---

## 🌳 Advanced: Connection Pooling
Senior engineers use **Connection Pools** to reuse database connections, saving the time it takes to "Handshake" with the database on every request.

**Real Use (High-Scale API)**:
A pool that keeps 5-10 connections open and ready for zero-latency traffic.

```python
from sqlalchemy import create_engine

# Expert Pattern: Pool Management. 
# 1. Reuses existing connections.
# 2. Prevents 'DB Exhaustion' by capping at 10.
engine = create_engine(
    "postgresql://user:pass@localhost/db",
    pool_size=10,
    max_overflow=20
)
```

---

## 🔥 Expert: Redis & Caching (The Cache-Aside Pattern)
Principal engineers use **Redis** (an in-memory database) to store "Hot Data" (like user sessions or frequent product info), reducing the load on the slower main Database.

```python
import redis
import json

# Connection to Redis
# cache = redis.Redis(host='localhost', port=6379, db=0)

def get_profile(user_id):
    """
    Principal Pattern: Cache-Aside. 
    1. Check Redis (Fast).
    2. If MISS, check DB (Slow).
    3. Update Redis for next time.
    """
    # r = cache.get(f"user:{user_id}")
    # if r: return json.loads(r)
```

---

## 🎯 Top 20 Principal Interview Questions (Database Engineering)

1. **Q: What is an ORM (Object-Relational Mapper)?**
   - **Answer**: A library (like SQLAlchemy) that allows you to interact with a database using Python objects instead of raw SQL strings. This makes code more maintainable, secure, and portable.
2. **Q: What is the 'N+1 Query Problem'?**
   - **Answer**: A performance issue where you fetch a list of 100 items and then make 100 *additional* queries to find the details for each. Solve it using **Joined Loading (JOIN)** in your ORM.
3. **Q: Explain 'Connection Pooling'.**
   - **Answer**: The practice of keeping a set of database connections open to be reused, rather than opening and closing a new connection for every single query, which is extremely expensive in terms of time and resources.
4. **Q: What is 'Redis' and why is it used alongside a SQL database?**
   - **Answer**: Redis is an **In-Memory** key-value store. It is used as a **Cache** for "Hot Data" to reduce the load on the slower persistent SQL database and decrease application latency.
5. **Q: What is 'SQL Injection' and how do ORMs prevent it?**
   - **Answer**: An attack where a user inputs malicious SQL commands. ORMs automatically use **Parameterized Queries**, which treat user input as data, not as executable commands.
6. **Q: Explain the 'Cache-Aside' pattern.**
   - **Answer**: The application checks the cache first. If the data is missing (Cache Miss), it fetches from the database and then **Updates** the cache for future requests.
7. **Q: What is a 'Database Migration' (e.g., Alembic)?**
   - **Answer**: A script that manages versioning for your database schema. It allows you to "Upgrade" or "Downgrade" the table structure safely across different environments (Dev, Prod).
8. **Q: What is 'ACID' in the context of databases?**
   - **Answer**: **A**tomicity, **C**onsistency, **I**solation, **D**urability — the 4 properties that guarantee a database transaction is processed reliably.
9. **Q: What is 'Database Indexing' and when should it be used?**
   - **Answer**: A copy of selected columns that allow for **O(1)** or **O(log n)** searching. Use it on columns that are frequently used in `WHERE` clauses (like `user_id` or `email`).
10. **Q: What is a 'Deadlock' in a database?**
    - **Answer**: When two transactions are waiting for each other to release a lock on a row, causing both to be stuck forever until the database engine terminates one of them.
11. **Q: Explain 'PostgreSQL' vs 'MySQL' for Python applications.**
    - **Answer**: **PostgreSQL** is generally preferred for its strict data integrity and superior support for JSON and advanced window functions. **MySQL** is known for its speed for simple read-heavy operations.
12. **Q: What is 'Database Replication'?**
    - **Answer**: The process of copying data from a "Leader" database to "Follower" databases to increase read-performance and provide high availability in case of a crash.
13. **Q: What is 'Sharding'?**
    - **Answer**: Splitting a massive database across multiple physical servers to handle more data and users than one machine could ever handle.
14. **Q: What is the purpose of a 'Transaction'?**
    - **Answer**: To group multiple operations (like withdrawing money and depositing it elsewhere) so they **either all succeed or all fail** together.
15. **Q: Explain 'Normalization' vs 'Denormalization'.**
    - **Answer**: **Normalization**: Reducing duplication (saving space). **Denormalization**: Intentionally adding duplication to **speed up reads** (common in high-scale systems).
16. **Q: What is 'Lazy Loading' in an ORM?**
    - **Answer**: Postponing the fetching of related data (like a user's orders) until that attribute is actually accessed in code.
17. **Q: What is the difference between 'SQL' and 'NoSQL'?**
    - **Answer**: **SQL**: Structured, schema-based, relational (Postgres). **NoSQL**: Flexible, document-based, non-relational (MongoDB).
18. **Q: What is the purpose of the `RETURNING` clause in SQL?**
    - **Answer**: To get data (like a newly generated ID) back from the database immediately after an `INSERT` or `UPDATE` operation.
19. **Q: How do you handle 'Database Downtime' in a Python app?**
    - **Answer**: Using a **Circuit Breaker** to stop making requests and showing a friendly "Service Unavailable" message instead of a generic 500 error.
20. **Q: What is a 'Stored Procedure' and why do modern engineers often avoid them?**
    - **Answer**: A function that lives inside the database. They are often avoided because they are harder to version control, monitor, and test compared to Python code.

---

[← Previous: Design Patterns](27-design-patterns-architecture.md) | [Next: Advanced Regex →](29-advanced-regex.md)
