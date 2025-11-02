# EXP-2: Word Count with RDD Operations

## 📝 Description

This experiment implements the classic "Word Count" problem using Apache Spark's RDD (Resilient Distributed Dataset) API. It demonstrates fundamental distributed computing concepts by reading a text file, processing it in parallel, and counting the frequency of each word.

## 🎯 Learning Objectives

- Understand RDD (Resilient Distributed Dataset) operations
- Learn the difference between transformations and actions
- Master `flatMap`, `map`, and `reduceByKey` operations
- Process text data with Spark
- Work with key-value pairs in distributed computing

## 📋 What This Program Does

1. **Creates SparkSession and SparkContext** - Initializes Spark application
2. **Reads Text File** - Loads `sample.txt` into an RDD
3. **Splits into Words** - Uses `flatMap` to break lines into individual words
4. **Creates Word Pairs** - Maps each word to `(word, 1)` tuple (case-insensitive)
5. **Aggregates Counts** - Uses `reduceByKey` to sum counts for each word
6. **Displays Results** - Collects and prints word frequencies
7. **Stops Spark** - Properly terminates the Spark session

## 📊 Sample Input

The program reads from `sample.txt`:

```
Hello World
Hello Spark
Big Data Processing
Spark is great for Big Data
Hello Big Data World
```

## 🚀 How to Run

### Prerequisites

Ensure you have:
- Python 3.8+
- PySpark installed (`uv sync` in project root)
- `sample.txt` file in the same directory

### Execution

```bash
# Navigate to the experiment directory
cd ~/projects/Big-Data-Spark/EXP-2

# Make sure sample.txt exists (it should be there already)
ls sample.txt

# Run the program
python exp2.py
```

### Using uv (from project root)

```bash
cd ~/projects/Big-Data-Spark
uv run python EXP-2/exp2.py
```

## 📤 Expected Output

```
hello 3
world 2
spark 2
big 3
data 3
processing 1
is 1
great 1
for 1
```

**Note:** Output order may vary since RDD operations are distributed across partitions.

## 🔍 Key Concepts Demonstrated

### 1. SparkContext
```python
sc = spark.sparkContext
```
- Low-level API for RDD operations
- Entry point for creating RDDs
- Required for text file operations

### 2. Reading Text Files
```python
lines = sc.textFile("sample.txt")
```
- Creates RDD from text file
- Each line becomes an element in the RDD
- Supports wildcards and directories

### 3. flatMap Transformation
```python
words = lines.flatMap(lambda line: line.split())
```
- Splits each line into words
- Flattens the result (one-to-many mapping)
- Example: `["Hello World"]` → `["Hello", "World"]`

### 4. map Transformation
```python
wordPairs = words.map(lambda word: (word.lower(), 1))
```
- Transforms each word to `(word, 1)` tuple
- Converts to lowercase for case-insensitive counting
- One-to-one mapping

### 5. reduceByKey Transformation
```python
wordCounts = wordPairs.reduceByKey(lambda a, b: a + b)
```
- Aggregates values for each key
- Combines counts: `(hello, 1) + (hello, 1) = (hello, 2)`
- Runs in parallel across partitions (efficient!)

### 6. collect Action
```python
wordCounts.collect()
```
- Triggers execution of all transformations
- Brings all results to driver program
- Returns Python list

## 🔧 Code Flow Visualization

```
sample.txt
    ↓ sc.textFile()
["Hello World", "Hello Spark", "Big Data Processing", ...]
    ↓ flatMap(split)
["Hello", "World", "Hello", "Spark", "Big", "Data", ...]
    ↓ map(word → (word.lower(), 1))
[("hello", 1), ("world", 1), ("hello", 1), ("spark", 1), ...]
    ↓ reduceByKey(add)
[("hello", 3), ("world", 2), ("spark", 2), ("big", 3), ...]
    ↓ collect()
Print results
```

## 💡 Modifications to Try

### 1. Filter Short Words
```python
words = lines.flatMap(lambda line: line.split()).filter(lambda word: len(word) > 3)
```

### 2. Sort by Count (Descending)
```python
sorted_counts = wordCounts.sortBy(lambda x: x[1], ascending=False)
for word, count in sorted_counts.collect():
    print(f"{word}: {count}")
```

### 3. Top 5 Most Frequent Words
```python
top5 = wordCounts.takeOrdered(5, key=lambda x: -x[1])
print("Top 5 words:", top5)
```

### 4. Remove Common Words (Stop Words)
```python
stop_words = ["is", "the", "a", "an", "for"]
words = lines.flatMap(lambda line: line.split()) \
             .filter(lambda word: word.lower() not in stop_words)
```

### 5. Count Total Words
```python
total_words = words.count()
print(f"Total words: {total_words}")
```

### 6. Remove Punctuation
```python
import string
words = lines.flatMap(lambda line: line.translate(str.maketrans('', '', string.punctuation)).split())
```

## 📊 Transformations vs Actions

### Transformations (Lazy)
- `flatMap()` - Splits and flattens
- `map()` - Transforms each element
- `reduceByKey()` - Aggregates by key
- `filter()` - Selects elements
- Not executed until an action is called

### Actions (Eager)
- `collect()` - Returns all elements to driver
- `count()` - Returns number of elements
- `take(n)` - Returns first n elements
- `saveAsTextFile()` - Writes to file
- Triggers execution of transformations

## 🐛 Troubleshooting

### Error: "sample.txt does not exist"
**Solution:**
```bash
cd ~/projects/Big-Data-Spark/EXP-2

# Create sample file
echo "Hello World Hello Spark" > sample.txt

# Run again
python exp2.py
```

### Error: "No module named 'pyspark'"
**Solution:**
```bash
cd ~/projects/Big-Data-Spark
uv sync
```

### Output Order Changes Each Run
- **This is normal!** RDD operations are distributed
- Use `sortBy()` or `sortByKey()` for consistent ordering

### Large File Performance Issues
- For very large files, avoid `collect()` (brings all data to driver)
- Use `take(n)` or write results to file instead
- Increase partitions: `sc.textFile("file.txt", minPartitions=8)`

## 📚 Related Concepts

- **MapReduce Pattern**: This program follows the classic MapReduce paradigm
- **Lazy Evaluation**: Transformations are not executed until an action is called
- **Distributed Computing**: Work is automatically distributed across partitions
- **Fault Tolerance**: RDDs can rebuild lost partitions using lineage information
- **In-Memory Processing**: Spark keeps data in memory for faster processing

## 🔗 Next Steps

After mastering this experiment, proceed to:
- **EXP-3**: Advanced RDD transformations and aggregation actions
- **EXP-7**: Understanding partitioning and data distribution
- **EXP-5**: DataFrame-based text processing (more optimized)

## 📖 Further Reading

- [RDD Programming Guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html)
- [Transformations and Actions](https://spark.apache.org/docs/latest/rdd-programming-guide.html#transformations)
- [MapReduce Pattern](https://en.wikipedia.org/wiki/MapReduce)
- [PySpark RDD API](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.html)

## 🎓 Interview Questions

**Q: What's the difference between `map` and `flatMap`?**  
A: `map` returns one element for each input element (1:1), while `flatMap` can return zero or more elements (1:N) and flattens the result.

**Q: Why use `reduceByKey` instead of `groupByKey`?**  
A: `reduceByKey` performs local aggregation before shuffling data, making it more efficient than `groupByKey` which shuffles all data first.

**Q: What happens if we don't call `collect()`?**  
A: Nothing! Transformations are lazy. Without an action like `collect()`, no computation is performed.

---

**Experiment Level:** Beginner  
**Estimated Time:** 10-15 minutes  
**Prerequisites:** Basic Python, understanding of lambda functions  
**Difficulty:** ⭐⭐☆☆☆
