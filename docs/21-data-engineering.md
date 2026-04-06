# 21. Data Engineering — Pandas, NumPy, Kafka & Spark

> "Data is the oil of the 21st century, but crude oil is useless. Expert data engineers use Python to refine it — cleaning, transforming, and optimizing trillions of rows across massive clusters without hitting memory bottlenecks."

---

## 🌱 The Basics: NumPy Arrays (NDArrays)
At the foundation of all data science in Python is **NumPy**. It provides high-performance arrays and math functions that are written in **C**.

**Real Use (Data/ML)**:
Efficiently performing math on 1 million data points at once.

```python
import numpy as np

# 1. Create 1 million random numbers
data = np.random.rand(1000000)

# 2. Vectorized Math: 100x faster than a 'for' loop!
result = data * 10
mean = np.mean(data)
```

---

## 🌿 Intermediate: Pandas (DataFrames)
`Pandas` is the standard for tabular data. It's like "Excel in Python."

- **DataFrame**: A table with rows and columns.
- **Series**: A single column.

```python
import pandas as pd

# Load from a CSV or Database
# df = pd.read_csv("telemetry.csv")

# 1. Filter for high latency
# high_latency = df[df['latency'] > 1.5]

# 2. Aggregations: Avg latency per service
# avg_per_svc = df.groupby('service')['latency'].mean()
```

---

## 🌳 Advanced: Kafka Streaming
Senior engineers use Python to process data **As It Happens** (Streaming) rather than every hour (Batch).

**Real Use (Streaming)**:
Sending a real-time event to a Kafka topic for processing.

```python
from confluent_kafka import Producer

def send_to_kafka(topic, message):
    """
    Expert Pattern: Data Ingestion. 
    Demonstrates: Real-time event production.
    """
    # p = Producer({'bootstrap.servers': 'localhost:9092'})
    # p.produce(topic, message.encode('utf-8'))
    # p.flush() # Wait for delivery
```

---

## 🔥 Expert: PySpark & Distributed Big Data
For principal-level engineering, you cannot process 1TB of data on one machine. You must use **PySpark** to distribute the work across 100 servers.

### 1. Lazy Execution
Spark doesn't run your code immediately. It builds a "Graph" (DAG) of your transformations and only executes when you ask for a result (`.show()` or `.collect()`).

```python
from pyspark.sql import SparkSession

# spark = SparkSession.builder.appName("LogProcessor").get_all()

# 1. Read from a S3 Data Lake (Parquet)
# Parquet is a 'Columnar' format that is 10x faster than CSV
# df = spark.read.parquet("s3://logs/raw_data/")

# 2. Transformation without loading to RAM!
# result = df.filter(df.status == 200).groupBy("ip").count()

# result.show()
```

---

## 🎯 Top 20 Principal Interview Questions (Data Engineering)

1. **Q: What is 'Vectorization' in NumPy/Pandas?**
   - **Answer**: It is the process of performing an operation on an entire array at once, rather than looping through individual items. Under the hood, this uses **SIMD** (Single Instruction, Multiple Data) on the CPU, making it thousands of times faster than a standard Python `for` loop.
2. **Q: When should you use Spark instead of Pandas?**
   - **Answer**: **Pandas** is great for data that fits in your server's RAM (usually 100MB to 10GB). **Spark** is for "Big Data" (100GB to 1TB+) that must be distributed across a cluster for parallel processing.
3. **Q: Explain 'Broadcasting' in NumPy.**
   - **Answer**: It allows NumPy to perform math operations between arrays and scalars (or arrays of different shapes) without making unnecessary copies of the data, saving massive amounts of RAM.
4. **Q: Why is 'Parquet' preferred over 'CSV' for Big Data?**
   - **Answer**: Parquet is **Columnar**. If you only need to calculate the average of one column in a 100-column table, Parquet allows you to skip reading 99% of the data. It also supports superior compression.
5. **Q: What is a 'Pandas Series' vs 'DataFrame'?**
   - **Answer**: A **Series** is a single column of data. A **DataFrame** is a 2D table composed of multiple Series (all sharing the same index).
6. **Q: How do you handle 'Missing Data' (NaN) in Pandas?**
   - **Answer**: By using `df.dropna()` to remove missing values or `df.fillna(value)` to replace them with a default or an average.
7. **Q: What is 'Lazy Execution' in PySpark?**
   - **Answer**: The strategy of not executing any code until an "Action" (like `.show()` or `.save()`) is called. This allows Spark's optimizer to combine multiple transformations into a highly efficient execution plan.
8. **Q: Explain the 'Shuffle' operation in distributed computing.**
   - **Answer**: A shuffle occurs when data needs to be moved between different servers (e.g., during a `groupBy`). It is the **most expensive** operation in Spark and should be minimized.
9. **Q: What is 'Kafka' and how is it used in Data Engineering?**
   - **Answer**: It is a distributed streaming platform that allows for **Real-Time Data Ingestion**. It acts as a high-speed "Buffer" between your data producers (apps) and your consumers (databases).
10. **Q: What is the difference between a 'List' and a 'NumPy Array'?**
    - **Answer**: A **List** can store multiple types and is an array of pointers (slow). A **NumPy Array** stores only one type (homogenous) and stores the data as a contiguous block in memory (extremely fast for math).
11. **Q: How do you read a 50GB CSV file in'Chunks' using Pandas?**
    - **Answer**: By passing `chunksize=10000` to `pd.read_csv()`. This returns an iterator that yields small DataFrames, preventing a `MemoryError`.
12. **Q: What is 'Method Chaining' in Pandas?**
    - **Answer**: A powerful syntax for combining operations: `df.dropna().groupby('A').sum().sort_values('B')`. It makes your code cleaner and more readable.
13. **Q: Explain 'SQL-Window Functions' in PySpark.**
    - **Answer**: They allow you to perform calculations across a set of rows that are related to the current row (e.g., finding a "Running Total" or a "Rank").
14. **Q: What is the purpose of 'NumPy Npy' format?**
    - **Answer**: It is a binary format that saves a NumPy array to disk exactly as it looks in memory, making it the fastest way to save and load numerical data.
15. **Q: What is 'Data Skew' and how does it impact Spark?**
    - **Answer**: It occurs when one partition of your data is much larger than the others (e.g., 90% of your users are from one country). This causes one server in your cluster to do all the work while others sit idle.
16. **Q: How do you use 'UDFs' (User Defined Functions) in PySpark?**
    - **Answer**: By using the `@udf` decorator. Warning: UDFs are slow because they force Spark to move data from JVM (Java) to Python and back. Always use built-in Spark SQL functions if possible.
17. **Q: What is the difference between `df.iloc` and `df.loc`?**
    - **Answer**: `iloc` is for **index-based** selection (integer positions). `loc` is for **label-based** selection (row/column names).
18. **Q: What is 'Data Normalization'?**
    - **Answer**: The process of re-scaling numerical data (e.g., ensuring all values are between 0 and 1) so that a machine learning model can process them more accurately.
19. **Q: Explain 'One-Hot Encoding'.**
    - **Answer**: Converting a categorical column (e.g., "Red", "Blue") into multiple binary columns (e.g., "IsRed", "IsBlue") so that it can be used in mathematical models.
20. **Q: How do you perform a 'Left Join' between two DataFrames?**
    - **Answer**: `pd.merge(df1, df2, on='key', how='left')`. It keeps all rows from the left table and adds matching data from the right.

---

[← Previous: CI/CD](20-python-ci-cd.md) | [Next: MLOps →](22-mlops.md)
