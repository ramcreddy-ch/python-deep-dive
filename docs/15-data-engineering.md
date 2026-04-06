# 15. Data Engineering — Pandas, PySpark & ETL Deep Dive

> Data engineering in Python is a battle against memory. Naive local scripting using Pandas is fine for 500MB datasets, but processing 5TB of clickstream logs daily requires distributed architectures, columnar formats, and lazy evaluation graphs.

---

## 🔍 Pandas (The Single Node Paradigm)

Pandas operates eagerly in memory. If your dataframe exceeds available RAM, your process is strictly OOM killed.

### Memory Optimization 101
The most expensive mistakes in Pandas are datatype assumptions.

```python
import pandas as pd

df = pd.read_csv("heavy_telemetry.csv")

# Problem 1: Pandas defaults all text to generic 'object' (Pointer to Python string)
# Very slow, massive memory.
print(df.memory_usage(deep=True))

# Fix: Convert low-cardinality text (like 'status', 'region') to Categorical
df['region'] = df['region'].astype('category') 
# Under the hood, this stores an array of small integers mapping to a lookup dictionary!
# Memory usage drops by up to 90%.

# Fix: Downcast generic 64-bit numbers
df['click_count'] = pd.to_numeric(df['click_count'], downcast='unsigned') # e.g., to uint8
```

### The Vectorization Rule
Never use `df.apply()` or `df.iterrows()` unless absolutely unavoidable. `iterrows()` is a Python-level `for` loop, eliminating all C-level speed advantages.

```python
# VERY BAD (1000x slower)
for index, row in df.iterrows():
    df.loc[index, 'total'] = row['price'] * row['tax']

# AVERAGE (Still uses Python function overhead per cell)
df['total'] = df.apply(lambda row: row['price'] * row['tax'], axis=1)

# PRODUCTION EXCELLENCE (Vectorized C-level array math)
df['total'] = df['price'] * df['tax']
```

---

## 🏭 PySpark (The Distributed Paradigm)

When data > RAM, we move to Apache Spark. PySpark is a Python API over a JVM (Scala) backend. It operates on **Lazy Evaluation**.

### Transformations vs Actions
Spark records your logic as a Directed Acyclic Graph (DAG). It computes *literally nothing* until an Action triggers execution.

```python
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

spark = SparkSession.builder.appName("ETLPipeline").getOrCreate()

# TRANSFORMATION: (Lazy) No data is loaded here.
df = spark.read.parquet("s3://bucket/massive-data/")

# TRANSFORMATION: (Lazy) DAG is updated, nothing computed.
filtered_df = df.filter(F.col("status") == "SUCCESS")\
                .groupBy("region")\
                .agg(F.sum("revenue").alias("total_rev"))

# ACTION: (Eager) The planner evaluates the DAG, optimizes it, and executes 
# across a cluster of 50 machines, returning the payload to the driver.
result = filtered_df.collect() 
```

### Addressing the Python-to-JVM Bottleneck (UDFs)
To run custom Python code against Spark DataFrame rows, we use User Defined Functions (UDFs). Historically, PySpark serialized data from the JVM -> passed to Python worker -> processed -> serialized -> back to JVM. This was cripplingly slow.

**Modern Solution: Pandas/Vectorized UDFs (Powered by Apache Arrow)**
Arrow facilitates zero-copy memory transfers between the JVM and Python.

```python
from pyspark.sql.functions import pandas_udf
import pandas as pd

# The function receives and returns Pandas Series natively
@pandas_udf("double")
def complex_math_udf(x: pd.Series, y: pd.Series) -> pd.Series:
    # Uses fast vectorized Pandas math rather than row-by-row
    return x * y + 3.14

# Executes extremely fast over Arrow memory formats
spark_df.withColumn("calculated", complex_math_udf("column_a", "column_b"))
```

---

## 🔧 Polars: The Modern Successor

Pandas is aging. It suffers from the GIL, excessive memory duplication, and lacks query optimization. **Polars** is written in Rust, natively utilizes all CPU cores, uses Arrow arrays internally, and has a lazy execution API.

```python
import polars as pl

# LAZY execution mode
query = (
    pl.scan_parquet("data.parquet") # Does not load file yet
    .filter(pl.col("age") > 30)
    .group_by("city")
    .agg(pl.col("salary").mean())
)

# Polars optimizes the query (e.g. Predicate Pushdown: it will only extract 
# the 'age', 'city', and 'salary' columns from the parquet file, ignoring the rest)
result_dataframe = query.collect() 
```

---

## 🎯 Senior Engineer Interview Questions

**Q1: In PySpark, explain the difference between `repartition()` and `coalesce()`. Which should you use to reduce partition count before writing to disk?**
> **Answer:** `coalesce()` minimizes data movement by combining existing partitions locally on nodes; it avoids a full cluster shuffle. `repartition()` forces a complete network shuffle to uniformly distribute data across nodes. If you are strictly *decreasing* the number of partitions before writing to an S3 bucket (to avoid creating 10,000 tiny files), you must use `coalesce()` to save massive network I/O overhead. You use `repartition()` only when you need to explicitly balance heavy skew or increase the partition count to utilize more cores.

**Q2: You have a Kafka topic emitting 100k events heavily skewed by `customer_id`. Your PySpark Structured Streaming job is dying due to OOMs on specific worker nodes. What is the architecture issue?**
> **Answer:** This is Data Skew. One or two massive `customer_id`s are sending 90% of the events, and because Spark partitions data for aggregations/joins via Hash Partitioning on the specific key, one worker node gets 90% of the data and crashes, while other nodes sit idle. The solution is "Salting". You artificially append a random integer (the 'salt') to the `customer_id` key during initial processing, which distributes the heavy customer across multiple nodes, perform the partial aggregation, remove the salt, and do a final global aggregation.

**Q3: Why shouldn't you append strings natively in a loop or use Pandas `df.append()`?**
> **Answer:** Strings and DataFrames are immutable blocks of memory. `df.append(new_row)` (depracated) or `concat` inside a heavy loop doesn't just add a row; it allocates an entirely new, larger block of RAM, copies all previous rows into it, adds the new row, and garbage-collects the old one. Over 10,000 iterations, this reaches $O(N^2)$ complexity. The correct approach is appending data to a native Python `list` of dictionaries, and constructing the final DataFrame exactly *once* at the end: `pd.DataFrame(list_of_dicts)`.

**Q4: What is Predicate Pushdown in the context of Parquet and ETL engines?**
> **Answer:** Predicate pushdown is a query engine optimization mechanism. If you write `SELECT name FROM data WHERE age > 50`, instead of loading the entire dataset into RAM and applying the filter, the engine (Spark/Polars) pushes the "predicate" (`age > 50`) down into the underlying storage layer reader. Because Parquet contains min/max statistics for every columnar block, it can completely skip reading blocks where `max_age < 50` natively from disk, reducing memory and I/O by orders of magnitude.

---

[← Previous: Networking & HTTP](14-networking-http.md) | [Back to Index](../README.md) | [Next: Machine Learning →](16-machine-learning.md)
