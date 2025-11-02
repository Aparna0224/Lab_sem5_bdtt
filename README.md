# Big Data Spark - Experiment Collection

This repository contains 7 Apache Spark experiments demonstrating various big data processing concepts using PySpark and Scala.

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Experiments Overview](#experiments-overview)
- [Installation Guide](#installation-guide)
- [Running the Experiments](#running-the-experiments)

---

## 🎯 Experiments Overview

### EXP-1: Basic DataFrame Operations
**File:** `EXP-1/exp1.py`

**What it does:**
- Creates a SparkSession
- Builds a DataFrame with student data (Name, Age, Department)
- Filters students from CSE department
- Displays filtered results

**Concepts:** DataFrame creation, filtering, selection, basic Spark SQL operations

---

### EXP-2: Word Count from Text File
**File:** `EXP-2/exp2.py`

**What it does:**
- Reads text from `sample.txt`
- Splits text into words
- Counts frequency of each word (case-insensitive)
- Displays word counts

**Concepts:** RDD operations, flatMap, map, reduceByKey, basic text processing

**⚠️ Note:** Requires `sample.txt` file in the same directory and SparkContext initialization

---

### EXP-3: RDD Transformations and Actions
**File:** `EXP-3/exp3.py`

**What it does:**
- Demonstrates comprehensive RDD operations
- **Retrieval Actions:** collect(), take(), takeSample(), takeOrdered(), top(), first(), isEmpty(), foreach()
- **Aggregation Actions:** count(), countByValue(), reduce(), fold(), aggregate()
- Calculates word counts and average word length
- Shows various ways to retrieve and process data from RDDs

**Concepts:** RDD transformations, actions, aggregations, data retrieval patterns

---

### EXP-4: Sparse Matrix Multiplication
**File:** `EXP-4/exp4.py`

**What it does:**
- Multiplies two sparse matrices using RDDs/MLlib CoordinateMatrix representation
- Keys entries, joins on the shared dimension, and reduces partial products to form the product
- Prints non-zero entries of the result

**Concepts:** Distributed matrix operations, MLlib, RDD joins and reductions

**Note:** The original example existed in Scala; a working PySpark version (`exp4.py`) is included so you can run it with Python like the other experiments. If you prefer the Scala variant you can convert/rename the file and run it with `spark-shell` or build a JAR.

---

### EXP-5: DataFrame Creation Methods & SQL Queries
**File:** `EXP-5/exp5.py`

**What it does:**
- Creates DataFrames from multiple sources:
  - List of tuples
  - RDD with custom schema
  - CSV file
- Demonstrates schema definition with StructType
- Executes SQL queries on DataFrames using temp views
- Shows aggregation with GROUP BY

**Concepts:** DataFrame creation, schema definition, Spark SQL, reading CSV files

**⚠️ Note:** Requires `people.csv` file in the same directory

---

### EXP-6: Real-time Stream Processing
**File:** `EXP-6/exp6.py`

**What it does:**
- Connects to a socket stream on localhost:9999
- Processes incoming text data in real-time (5-second batches)
- Counts word frequency in each streaming batch
- Displays results continuously

**Concepts:** Spark Streaming, DStream, real-time data processing, micro-batching

**⚠️ Note:** Requires netcat running: `nc -lk 9999` in a separate terminal

---

### EXP-7: RDD Partitioning
**File:** `EXP-7/exp7.py`

**What it does:**
- Creates RDD with numbers 1-20
- Demonstrates partition inspection
- Shows `repartition()` operation (full shuffle, increases partitions)
- Shows `coalesce()` operation (optimized, decreases partitions)
- Displays data distribution across partitions

**Concepts:** Partitioning strategies, repartition vs coalesce, data distribution optimization

---

## 📦 Prerequisites

### Required Software

1. **Java Development Kit (JDK)**
   - JDK 8 or JDK 11 (recommended for Spark)
   - Set `JAVA_HOME` environment variable

2. **Python**
   - Python 3.7 or higher
   - pip (Python package manager)

3. **Apache Spark** (Optional if using PySpark package)
   - Download from [spark.apache.org](https://spark.apache.org/downloads.html)
   - Set `SPARK_HOME` environment variable

4. **Scala & sbt** (Only for EXP-4)
   - Scala 2.12.x
   - sbt (Scala Build Tool)

---

## 🔧 Installation Guide

### 1. Install Python Packages

```bash
pip install pyspark findspark
```

### 2. Verify Installation

```bash
# Check Python
python --version

# Check Java
java -version

# Check PySpark
python -c "import pyspark; print(pyspark.__version__)"
```

### 3. Create Required Data Files

**For EXP-2:** Create `sample.txt` in `EXP-2/` directory:
```bash
cd EXP-2
echo "Spark is amazing Spark is fast Spark makes big data easy" > sample.txt
```

**For EXP-5:** Create `people.csv` in `EXP-5/` directory:
```bash
cd EXP-5
echo "name,age" > people.csv
echo "John,28" >> people.csv
echo "Alice,30" >> people.csv
echo "Bob,25" >> people.csv
```

---

## ▶️ Running the Experiments

### Running Python Experiments (EXP-1, 2, 3, 5, 6, 7)

```bash
# Navigate to experiment folder
cd EXP-1

# Run the experiment
python exp1.py
```

### Running EXP-6 (Streaming)

**Terminal 1 - Start netcat:**
```bash
nc -lk 9999
```

**Terminal 2 - Run the program:**
```bash
cd EXP-6
python exp6.py
```

**Type text in Terminal 1** and see word counts in Terminal 2

### Running EXP-4 (Scala)

```bash
cd EXP-4

# Rename file
mv exp4.py exp4.scala

# Compile and run with sbt or spark-submit
scalac exp4.scala
# Or use spark-submit with compiled JAR
```

---

## 🐛 Troubleshooting

### Common Issues

1. **"Java is not recognized"**
   - Install JDK and set JAVA_HOME

2. **"pyspark module not found"**
   - Run: `pip install pyspark`

3. **EXP-2 fails**
   - Ensure `sample.txt` exists
   - Fix SparkContext initialization (see code)

4. **EXP-5 fails**
   - Create `people.csv` file

5. **EXP-6 connection refused**
   - Start netcat first: `nc -lk 9999`

---

## 📚 Learning Outcomes

After completing these experiments, you will understand:
- ✅ DataFrame vs RDD operations
- ✅ Data transformations and actions
- ✅ Real-time stream processing
- ✅ Partitioning and optimization
- ✅ Spark SQL queries
- ✅ Matrix operations in distributed systems
- ✅ Different data input/output methods

---

## 📝 Notes

- All Python experiments use PySpark API
- EXP-4 is written in Scala (despite .py extension)
- Some experiments require input files (check individual descriptions)
- Use WSL/Linux environment for best compatibility
- Experiments run in local mode (no cluster required)

---

## 🤝 Contributing

Feel free to extend these experiments with:
- Additional data sources
- More complex transformations
- Performance optimizations
- Real-world datasets

---

## 📄 License

Educational purposes - Apache Spark examples

---

**Happy Learning with Apache Spark! 🚀**
