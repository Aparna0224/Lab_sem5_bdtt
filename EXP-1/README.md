# EXP-1: Basic Spark DataFrame Operations

## 📝 Description

This experiment demonstrates the fundamental operations of Apache Spark using DataFrames. It covers creating a Spark session, building a DataFrame from scratch, filtering data, and displaying results.

## 🎯 Learning Objectives

- Understand how to create a SparkSession
- Learn DataFrame creation from Python collections
- Practice filtering operations on DataFrames
- Perform column selection
- Display DataFrame results

## 📋 What This Program Does

1. **Creates a SparkSession** - Initializes the Spark application with name "BasicSparkApp"
2. **Builds a DataFrame** - Creates a structured dataset with student information:
   - Name (String)
   - Age (Integer)
   - Department (String)
3. **Filters Data** - Selects only students from the "CSE" department
4. **Selects Columns** - Displays only "Name" and "Age" columns
5. **Shows Results** - Prints the filtered data in a formatted table
6. **Stops Spark** - Properly terminates the Spark session

## 📊 Sample Data

The program uses this sample dataset:

| Name    | Age | Department |
|---------|-----|------------|
| Alice   | 22  | CSE        |
| Bob     | 25  | ECE        |
| Charlie | 23  | CSE        |
| David   | 21  | MECH       |

## 🚀 How to Run

### Prerequisites

Ensure you have installed:
- Python 3.8+
- PySpark (`pip install pyspark` or `uv sync` in project root)

### Execution

```bash
# Navigate to the experiment directory
cd ~/projects/Big-Data-Spark/EXP-1

# Run the program
python exp1.py
```

### Using uv (from project root)

```bash
cd ~/projects/Big-Data-Spark
uv run python EXP-1/exp1.py
```

## 📤 Expected Output

```
+-------+---+
|   Name|Age|
+-------+---+
|  Alice| 22|
|Charlie| 23|
+-------+---+
```

**Explanation:** Only students from the CSE department (Alice and Charlie) are displayed with their names and ages.

## 🔍 Key Concepts Demonstrated

### 1. SparkSession
```python
spark = SparkSession.builder.appName("BasicSparkApp").getOrCreate()
```
- Entry point for DataFrame and SQL functionality
- `.builder` - Creates a builder for SparkSession
- `.appName()` - Sets the application name
- `.getOrCreate()` - Gets existing session or creates new one

### 2. DataFrame Creation
```python
df = spark.createDataFrame(data, columns)
```
- Creates DataFrame from list of tuples
- Automatically infers data types
- Structured data with named columns

### 3. Filtering
```python
df.filter(df.Department == "CSE")
```
- Filters rows based on condition
- Uses column reference syntax (`df.ColumnName`)
- Returns new DataFrame (transformation is lazy)

### 4. Column Selection
```python
.select("Name", "Age")
```
- Projects specific columns
- Can reorder columns
- Reduces data size by excluding unwanted columns

### 5. Action
```python
result.show()
```
- Triggers execution of transformations
- Displays formatted output
- Default shows 20 rows

## 🔧 Code Structure

```python
# Step 1: Initialize Spark
spark = SparkSession.builder.appName("BasicSparkApp").getOrCreate()

# Step 2: Prepare data
data = [(...), (...), ...]
columns = ["Name", "Age", "Department"]

# Step 3: Create DataFrame
df = spark.createDataFrame(data, columns)

# Step 4: Transform and filter
result = df.filter(...).select(...)

# Step 5: Display results
result.show()

# Step 6: Cleanup
spark.stop()
```

## 💡 Modifications to Try

### 1. Filter by Age
```python
result = df.filter(df.Age > 22).select("Name", "Department")
```

### 2. Multiple Conditions
```python
result = df.filter((df.Department == "CSE") & (df.Age < 23))
```

### 3. Add More Columns
```python
result = df.filter(df.Department == "CSE").select("Name", "Age", "Department")
```

### 4. Sort Results
```python
result = df.filter(df.Department == "CSE").orderBy("Age", ascending=False).select("Name", "Age")
```

### 5. Count Results
```python
count = df.filter(df.Department == "CSE").count()
print(f"CSE students: {count}")
```

## 🐛 Troubleshooting

### Error: "No module named 'pyspark'"
**Solution:**
```bash
pip install pyspark
# or
cd ~/projects/Big-Data-Spark && uv sync
```

### Error: "JAVA_HOME is not set"
**Solution:**
```bash
# Install Java
sudo apt install openjdk-11-jdk

# Set JAVA_HOME (add to ~/.bashrc)
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$PATH:$JAVA_HOME/bin
```

### Spark Takes Too Long to Start
- First run downloads dependencies (normal)
- Subsequent runs are faster
- Running in local mode is slower than cluster mode

## 📚 Related Concepts

- **Lazy Evaluation**: Transformations are not executed until an action is called
- **DataFrame vs RDD**: DataFrames provide higher-level API with optimizations
- **Catalyst Optimizer**: Spark automatically optimizes DataFrame operations
- **Immutability**: Each transformation creates a new DataFrame

## 🔗 Next Steps

After mastering this experiment, proceed to:
- **EXP-2**: Word count with RDD operations
- **EXP-3**: Advanced RDD transformations and actions
- **EXP-5**: More DataFrame creation methods and SQL queries

## 📖 Further Reading

- [Spark DataFrame Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [PySpark API Documentation](https://spark.apache.org/docs/latest/api/python/)
- [DataFrame Operations](https://spark.apache.org/docs/latest/sql-getting-started.html)

---

**Experiment Level:** Beginner  
**Estimated Time:** 5-10 minutes  
**Prerequisites:** Basic Python knowledge
