# 21. Data Engineering — Pandas, Kafka & Scalable Pipelines

> "Data is the 'New Oil,' but raw oil is useless; it must be refined. An expert doesn't just 'read a CSV'; they build resilient, streaming pipelines that transform billions of rows into actionable intelligence without ever crashing the system."

---

## ❓ The 'Why' (High-Level)
In the age of "Big Data," the challenge isn't storing data—it's **Moving and Transforming** it. A modern enterprise has data in SQL databases, S3 buckets, and millions of IoT sensors. **Data Engineering** is the art of building the "Plumbing" (ETL: Extract, Transform, Load) that connects these sources. A principal engineer knows that a single slow loop in a data pipeline can turn a 1-hour job into a 1-week nightmare.

---

## 🌱 Module 1: The Basics (Junior) — The `Pandas` Foundation
Pandas is the core library for data manipulation in Python.

### 1. DataFrames & Series
- **Series**: A single column of data.
- **DataFrame**: A table (like an Excel sheet) with rows and columns.

### 2. Loading and Filtering
```python
import pandas as pd
df = pd.read_csv("sales.csv")

# Only look at high-value sales
high_value = df[df["amount"] > 1000]
print(high_value.head())
```

---

## 🌿 Module 2: Professional Mastery (Mid-Level) — Transformation
Mid-level engineers clean and join data from multiple sources.

### 1. GroupBy & Aggregation
Summarize millions of rows in milliseconds.
```python
# Average price per category
results = df.groupby("category")["price"].mean()
```

### 2. Handling Missing Data (`NaN`)
Real data is messy. You must decide whether to fill holes or delete them.
- **Expert fix**: `df.fillna(method='ffill')` or `df.dropna()`.

---

## 🌳 Module 3: Advanced Mechanics (Senior) — Streaming with Kafka
Senior engineers move from "Batch" (once a day) to "Real-Time" (every second).

### 1. Apache Kafka: The Backbone
Kafka is a "Message Queue" that can handle trillions of events.
- **Producer**: A script that sends events (e.g., "User clicked a button").
- **Consumer**: A script that reads events and saves them to a database.

### 2. Parquet vs. CSV
In production, we never use CSV for large data. **Parquet** is a binary "Columnar" format that is 10x smaller and 50x faster to read because it only loads the columns you ask for.

---

## 🔥 Module 4: Principal Architect (Principal) — Architecture at Scale
At the highest level, you choose the "Blueprint" for the entire company's data.

### 1. Lambda vs Kappa Architecture
- **Lambda**: Running both a fast "Real-time" pipeline and a slow, accurate "Batch" pipeline.
- **Kappa**: Everything is a "Stream." Use one single logic for both real-time and historical data.

### 2. Vectorization (No Loops!)
A principal engineer **never** uses `for row in dataframe`. That is 1,000x slower.
- **The Expert Way**: Use **Vectorized Operations** (NumPy under the hood) that perform math on the whole column at once using the CPU's specialized instructions (SIMD).

---

## 🏗️ Case Study: The Billion-Transaction Pipeline
A global payment processor needed to detect fraud across 1 billion transactions per day.
- **The Junior Approach**: A Python script that read transactions from a database and checked them in a loop. (System fell 48 hours behind in the first day).
- **The Principal Approach**: Used **Kafka** to stream transactions and **Spark (PySpark)** to perform real-time windowing to check "How many times did this card zip across 5 different cities in 10 minutes?"
- **Result**: Fraud detection happened in **under 500ms**, saving the company $2 million in fraudulent charges per day.

---

## ⚡ Anti-Patterns & Expert Traps

### 1. The `iterrows()` Death-Trap
Never use `.iterrows()` to loop over a Pandas DataFrame. It's the slowest possible way to process data. **Expert fix**: Use `.apply()` or, even better, vectorized functions like `df['a'] + df['b']`.

### 2. Loading Everything into RAM
If your file is 100GB and your RAM is 16GB, `pd.read_csv()` will crash. **Expert fix**: Use the `chunksize` parameter to process the file in 10,000-row pieces.

---

## 🎯 Top 20 Principal Interview Questions (Data Engineering)

1. **Q: What is the difference between a DataFrame and a Series?**
   - **Answer**: A **Series** is a 1-dimensional array (like a column). A **DataFrame** is a 2-dimensional tabular structure (like a table) composed of multiple Series.
2. **Q: Why is 'Parquet' preferred over 'CSV' for Big Data?**
   - **Answer**: Parquet is a **Columnar** binary format. It is highly compressed and allows for "Predicate Pushdown" (only reading the specific columns and rows you need), which is much faster than reading a whole CSV.
3. **Q: What is 'Vectorization' in Pandas?**
   - **Answer**: The process of performing math on an entire array at once using low-level C and SIMD instructions, rather than using a Python `for` loop. It's often 100x-1,000x faster.
4. **Q: Explain 'ETL' vs 'ELT'.**
   - **Answer**: **ETL** (Extract, Transform, Load): Transforming data before it hits the warehouse. **ELT** (Extract, Load, Transform): Dumping raw data into the warehouse (like Snowflake/BigQuery) and using the warehouse's power to transform it.
5. **Q: What is 'Lambda Architecture'?**
   - **Answer**: A data processing architecture designed to handle massive quantities of data by providing both a "Batch Layer" (for high accuracy) and a "Speed Layer" (for low latency).
6. **Q: Explain 'Schema on Read' vs 'Schema on Write'.**
   - **Answer**: **Schema on Write**: Defining the format before saving (SQL). **Schema on Read**: Saving raw data and defining the format only when you read it (Data Lakes/Hadoop).
7. **Q: What is a 'Data Lake'?**
   - **Answer**: A central repository that allows you to store all your structured and unstructured data at any scale (usually in S3 or Azure Blob) in its raw format.
8. **Q: How does 'Apache Kafka' handle backpressure?**
   - **Answer**: Kafka is a **Pull-based** system. The "Consumer" asks for data when it's ready. If the consumer is slow, data just sits safely in the Kafka logs (retention) without overwhelming the receiver.
9. **Q: What is the difference between a 'Narrow' and a 'Wide' transformation in Spark?**
   - **Answer**: **Narrow**: Data from one partition is needed (e.g., `map`, `filter`). **Wide**: Data from many partitions is needed, requiring a "Shuffle" (e.g., `groupBy`, `join`). Wide transformations are much more expensive.
10. **Q: How do you handle 'Data Skew' in a distributed join?**
    - **Answer**: By "Salting" the keys—adding a random number to the key to force it to be distributed across more workers, preventing a single worker from being overloaded by one massive key.
11. **Q: What is a 'Window Function' in streaming?**
    - **Answer**: A way to perform aggregations over a specific time range (e.g., "Average price over the last 5 minutes") as data flows through the system.
12. **Q: Why should you avoid `df.iterrows()`?**
    - **Answer**: Because it creates a new Series object for every single row, which is incredibly slow in Python. Use vectorized operations or `.apply()` instead.
13. **Q: What is the purpose of 'Apache Airflow'?**
    - **Answer**: To **Schedule and Monitor** complex workflows (DAGs) of data pipelines, ensuring that Stage B only starts after Stage A has successfully finished.
14. **Q: Explain 'Data Lineage'.**
    - **Answer**: The audit trail of data from its origin to its destination, showing exactly what transformations were applied at every step. This is critical for security and debugging.
15. **Q: What is 'CDC' (Change Data Capture)?**
    - **Answer**: A technique to capture and stream any "Changes" (Insert, Update, Delete) from a database in real-time, often using tools like **Debezium**.
16. **Q: How does `Pandas` handle memory?**
    - **Answer**: It loads data into **RAM**. For datasets larger than RAM, you must use "Chunking," "Dask" (which scales Pandas), or a different tool like Spark.
17. **Q: What is 'Normalizing' vs 'Denormalizing' data?**
    - **Answer**: **Normalizing**: Reducing redundancy by splitting data into multiple tables (best for SQL). **Denormalizing**: Combining data into one large table (best for Big Data reads/NoSQL).
18. **Q: What is the benefit of a 'Feature Store' in data engineering?**
    - **Answer**: A centralized place to store transformed data "Features" so they can be reused across multiple machine learning models without re-calculating them.
19. **Q: Explain 'At-least-once' vs 'Exactly-once' delivery.**
    - **Answer**: **At-least-once**: Data might be sent again if an error occur (duplicates possible). **Exactly-once**: The system guarantees data is processed only once, which is much harder to achieve.
20. **Q: How do you optimize a `join` operation in Pandas?**
    - **Answer**: By ensuring both DataFrames are sorted by the join key and using the correct join type (Inner, Left, Right, Outer) to minimize the resulting dataset size.

---

[Previous: CI/CD](20-python-ci-cd.md) | [Next: MLOps →](22-mlops.md)
