# 28. Database Engineering — SQLAlchemy, Redis & Performance Tuning

> "Data is the lifeblood of an application. An expert doesn't just 'save to a database'; they understand 'Query Optimization', 'Indexing', 'Locking', and the trade-offs between SQL and NoSQL. A single missing index can turn a 1-millisecond query into a 10-second nightmare."

---

## ❓ The 'Why' (High-Level)
Your Python code is temporary—it disappears when the server restarts. Your **Database** is permanent. In a large system, the database is almost always the **Bottleneck**. A principal engineer knows how to design "Schemas" that grow from 100 users to 100 million without collapsing. They know when to use **SQL** (for reliability) and when to use **NoSQL** (for massive scale).

---

## 🌱 Module 1: The Basics (Junior) — Talking to SQL
Most apps start with a simple Relational Database (SQL).

### 1. The Survival Kit: SQLite
Python comes with **SQLite** built-in. It's a "File-based" database that's perfect for small apps and local testing.
```python
import sqlite3
# Create a connection and a table
conn = sqlite3.connect('example.db')
conn.execute("CREATE TABLE users (id INTEGER, name TEXT)")
```

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — The ORM
Mid-level engineers use an **ORM (Object-Relational Mapper)** to write Python instead of raw SQL strings.

### 1. SQLAlchemy
It allows you to treat a database table as a **Python Class**.
```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
```

### 2. Migrations (Alembic)
Professional developers never manually change the database. They use **Alembic** to "Version Control" the database schema, allowing them to "Upgrade" or "Rollback" changes.

---

## 🌳 Module 3: Advanced Mechanics (Senior) — Optimization
Senior engineers fix the "Slow" queries before they reach production.

### 1. Indexing (The Secret to Speed)
An **Index** is like the index at the back of a book. Without it, the database must read **every single row** to find one user.
- **Expert fix**: `Column(String, index=True)`.

### 2. The N+1 Query Problem
A common mistake where you fetch 100 users, and then make **100 more separate calls** to get each user's address.
- **Expert fix**: Use `joinedload()` in SQLAlchemy to fetch everything in **one** single SQL query.

---

## 🔥 Module 4: Principal Architect (Principal) — Scaling & Caching
At the highest level, you manage "Distributed Data."

### 1. Read Replicas & Sharding
- **Read Replicas**: Having one "Master" database for writing data and 10 "Replica" databases for reading data.
- **Sharding**: Splitting a massive table (e.g., "Transactions") across 5 different servers based on a key (like `user_id`).

### 2. Fast Caching with Redis
Storing "Hot Data" (like the current number of likes on a post) in **Redis**, an in-memory database that is 1,000x faster than SQL.

---

## 🏗️ Case Study: The Black Friday Surge
An e-commerce site crashed every year on Black Friday because the "Product Search" was too slow.
- **The Junior Approach**: Add more web servers. (Didn't work; the database was actually the bottleneck).
- **The Principal Approach**: Ran an `EXPLAIN` on the search query, discovered a missing index on the `category` column, and implemented a **Redis Cache** for the top 100 trending products.
- **Result**: Database load dropped by **90%**, and the site stayed up during the busiest hour of the year.

---

## ⚡ Anti-Patterns & Expert Traps

### 1. Hardcoding SQL Strings
**NEVER** do `f"SELECT * FROM users WHERE name='{name}'"`. This is an invitation for **SQL Injection**. Always use the ORM or parameterized queries.

### 2. Over-Indexing
If you add an index to **EVERY** column, your "Reads" will be fast, but your "Writes" will be incredibly slow because the database has to update 50 indexes for every new row. **Expert fix**: Only index the columns you actually search for.

---

## 🎯 Top 20 Principal Interview Questions (Database Engineering)

1. **Q: What is an ORM and why use one?**
   - **Answer**: **Object-Relational Mapper**. It allows you to interact with a database using Python objects instead of raw SQL. This makes the code more readable, easier to test, and protects against SQL injection.
2. **Q: Explain the 'N+1 Query Problem'.**
   - **Answer**: A performance anti-pattern where a program makes one query to get a list of items and then many subsequent queries to get related data for each item. It is solved using **Eager Loading** (Joining).
3. **Q: What is a 'Database Index' and how does it work?**
   - **Answer**: A data structure (usually a B-Tree) that provides a "Fast Look-up" for specific columns. It prevents the database from performing a "Full Table Scan" (reading every row).
4. **Q: What are the 'ACID' properties of a transaction?**
   - **Answer**: **Atomicity** (All or nothing), **Consistency** (Valid state), **Isolation** (No interference), **Durability** (Saved forever).
5. **Q: What is the difference between SQL (Relational) and NoSQL?**
   - **Answer**: **SQL**: Fixed schema, strict relationships, best for reliable transactions. **NoSQL**: Flexible schema, horizontally scalable, best for massive collections of unstructured data.
6. **Q: What is 'Alembic' or 'Flyway' used for?**
   - **Answer**: For **Database Migrations**. It tracks the history of changes to the database schema, ensuring that every developer and server has the exact same database structure.
7. **Q: Explain the 'CAP' Theorem.**
   - **Answer**: In a distributed system, you can only have two of the three: **Consistency**, **Availability**, and **Partition Tolerance**. Architects must choose the right balance.
8. **Q: What is 'Connection Pooling'?**
   - **Answer**: Keeping a collection of open database connections ready to be reused, rather than opening and closing a new one for every single request (which is very expensive).
9. **Q: What is 'Redis' and when should you use it?**
   - **Answer**: An **In-Memory** key-value store. used it for **Caching**, **Session Management**, or as a **Message Broker** where sub-millisecond response times are required.
10. **Q: What is 'Database Sharding'?**
    - **Answer**: Splitting a large dataset across multiple physical database servers based on a key (e.g., users A-M on Server 1, N-Z on Server 2) to scale horizontally.
11. **Q: Explain 'Deadlock' in a database.**
    - **Answer**: A situation where Transaction A holds a lock that Transaction B needs, and B holds a lock that A needs. Neither can finish, and they are stuck forever until the DB kills one.
12. **Q: What is the difference between 'Inner Join' and 'Outer Join'?**
    - **Answer**: **Inner**: Returns only rows where there is a match in both tables. **Outer**: Returns all rows from one table, plus matching rows from the other (filling with NULL if no match).
13. **Q: What is a 'Database View'?**
    - **Answer**: A virtual table initiated by a query. It doesn't store data itself but provides a simplified way to access complex, multi-table joins.
14. **Q: Explain 'Database Normalization'.**
    - **Answer**: The process of organizing data into multiple tables to minimize redundancy and dependency (e.g., 1NF, 2NF, 3NF).
15. **Q: What is a 'Stored Procedure'?**
    - **Answer**: A set of SQL statements that are saved and executed directly on the database server. While fast, they are harder to version control and test than Python code.
16. **Q: What is 'Soft Delete'?**
    - **Answer**: Instead of deleting a row, you set a `deleted_at` timestamp. This allows for data "Undeleting" and keeps an audit trail, but requires filtering in every query.
17. **Q: Explain 'Constraint' (e.g., Unique, Not Null, Foreign Key).**
    - **Answer**: Rules enforced by the database to ensure data integrity (e.g., preventing two users from having the same email address).
18. **Q: What is 'Explain Analyze'?**
    - **Answer**: A command used to see exactly how the database executes a query (e.g., which indexes it uses, how many rows it scans). It is the primary tool for query optimization.
19. **Q: What is 'Write-Ahead Logging' (WAL)?**
    - **Answer**: A standard method for ensuring data durability by writing changes to a simple log file **before** updating the actual database data files.
20. **Q: What is a 'Composite Index'?**
    - **Answer**: An index that covers more than one column (e.g., an index on `first_name` AND `last_name`). Useful for queries that always filter on both fields simultaneously.

---

[Previous: Design Patterns](27-design-patterns-solid.md) | [Next: Advanced Regex →](29-advanced-regex.md)
