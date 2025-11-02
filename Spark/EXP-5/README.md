# EXP-5: DataFrame Creation & Spark SQL

## 📝 Description

This experiment demonstrates several ways to create Spark DataFrames and run simple Spark SQL queries. The script `exp5.py` shows:

- Creating a DataFrame from a list of tuples
- Creating a DataFrame from an RDD with a defined schema
- Reading a CSV into a DataFrame (`people.csv`) with header + schema inference
- Registering a temporary view and running a SQL query (GROUP BY)

The `people.csv` in this folder includes columns: `name, age, city` and is used by the CSV-reading example.

## 🎯 Learning objectives

- Learn multiple DataFrame creation methods in PySpark
- Define and apply an explicit schema using `StructType`
- Read CSV files into DataFrames with `header=True` and `inferSchema=True`
- Use Spark SQL by registering temporary views
- Inspect DataFrame schema and data using `.show()` and `.printSchema()`

## Files

- `exp5.py` — example script demonstrating DataFrame creation and SQL
- `people.csv` — sample CSV used by the script (header: `name,age,city`)

## ▶️ How to run

### Prerequisites

- Python 3.8+
- PySpark installed in the active environment (`pip install pyspark`) or use `spark-submit` with a Spark distribution
- `people.csv` present in the `EXP-5` directory (this repo already includes one)

### Run with Python (in your virtualenv)

```bash
cd ~/projects/Big-Data-Spark/EXP-5
python exp5.py
```

### Or run with Spark's spark-submit (recommended for consistent Spark environment)

```bash
cd ~/projects/Big-Data-Spark/EXP-5
$SPARK_HOME/bin/spark-submit --master local exp5.py
```

## 📤 What `exp5.py` does (step-by-step)

1. Creates a `SparkSession`.
2. Creates `df1` from a list of tuples and prints it and its schema.
3. Creates an RDD, defines a `StructType` schema, converts the RDD to `df2`, and prints it.
4. Reads `people.csv` into `dfcsv` using `spark.read.csv("people.csv", header=True, inferSchema=True)` and prints it and its schema.
5. Registers `df1` as a temporary view `people` and runs a SQL aggregation:

```sql
SELECT age, COUNT(*) AS cnt FROM people GROUP BY age
```

6. Stops the Spark session.

## 📤 Expected output (example)

Running `python exp5.py` should show three DataFrame prints and schema outputs, followed by the SQL aggregation. With the provided `people.csv` (names, ages, cities), sample output looks like:

```
+-----+---+
| name|age|
+-----+---+
| John| 28|
|Alice| 30|
|  Bob| 25|
| Maria| 27|
|  ...|
+-----+---+

root
 |-- name: string (nullable = true)
 |-- age: integer (nullable = true)

+----+---+-------------+
|name|age|       city  |
+----+---+-------------+
|John| 28|     New York|
|Alice|30|San Francisco|
|... |...|         ... |
+----+---+-------------+

root
 |-- name: string (nullable = true)
 |-- age: integer (nullable = true)
 |-- city: string (nullable = true)

+---+---+
|age|cnt|
+---+---+
| 28|  1|
| 30|  1|
| 25|  1|
| ...|
+---+---+
```

Exact row order and formatting may vary.

## 🔧 Frequently seen issues & fixes

- `ModuleNotFoundError: No module named 'pyspark'`
  - Install with `pip install pyspark` in your active environment, or run the script with `spark-submit` from a Spark installation.

- `JAVA_HOME` or Java errors
  - Make sure a JDK (8 or 11) is installed and `JAVA_HOME` points to it. On Ubuntu/WSL:
    ```bash
    sudo apt update && sudo apt install openjdk-11-jdk
    export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
    export PATH=$JAVA_HOME/bin:$PATH
    ```

- `FileNotFoundError: people.csv`
  - Ensure you run the script from the `EXP-5` directory or use an absolute path in the `read.csv()` call.

- Schema inference wrong/missing columns
  - If inference fails, provide an explicit schema using `StructType/StructField` like the example in `exp5.py`.

## 💡 Modifications & experiments to try

- Add more fields to `people.csv` (e.g., `occupation`) and re-run to see schema changes.
- Persist `dfcsv` results to Parquet to observe speed and schema preservation:

```python
dfcsv.write.mode("overwrite").parquet("out/people.parquet")
```

- Run more complex SQL queries (JOINs, window functions) by creating additional DataFrames and registering them as views.

## 📚 Further reading

- Spark DataFrame Guide: https://spark.apache.org/docs/latest/sql-programming-guide.html
- PySpark DataFrame API: https://spark.apache.org/docs/latest/api/python/

---

If you'd like, I can also:
- Add an example that writes `dfcsv` to Parquet and reads back to verify.
- Add unit tests that validate schema and row counts.
Which would you like next?