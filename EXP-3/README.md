# EXP-3: RDD Transformations and Actions

## 📝 Description

This experiment demonstrates core RDD (Resilient Distributed Dataset) operations in PySpark. It shows common transformations (lazy) and actions (which trigger computation) using a small in-memory dataset of sentences.

## 🎯 Learning Objectives

- Understand the difference between transformations and actions
- Learn and practice `flatMap`, `map`, `reduceByKey`, and `filter`
- Explore retrieval actions like `collect`, `take`, `takeSample`, `takeOrdered`, `top`, `first`, `isEmpty`, and `foreach`
- Explore aggregation actions like `count`, `countByValue`, `reduce`, `fold`, and `aggregate`
- Calculate simple aggregation metrics (e.g., average word length)

## 📋 What This Program Does

1. Initializes a `SparkContext` in local mode
2. Creates an RDD from a small list of sentences
3. Uses `flatMap` to split sentences into words
4. Maps words to `(word, 1)` pairs and reduces by key to count occurrences
5. Filters counts to show words with frequency > 1
6. Demonstrates many retrieval and aggregation actions and prints results

## ▶️ How to Run

### Prerequisites
- Python 3.8+
- PySpark installed in your environment (`pip install pyspark` or `uv sync` from project root)

### Run the script

```bash
cd ~/projects/Big-Data-Spark/EXP-3
python exp3.py
```

This script doesn't require any external input files.

## 📤 Expected Output (example)

You will see multiple sections printed. Example output:

```
--- Retrieval Actions ---
Collect: ['Spark', 'is', 'fast', 'Spark', 'is', 'powerful', 'Spark', 'is', 'easy', 'to', 'use']
Take(5): ['Spark', 'is', 'fast', 'Spark', 'is']
TakeSample (no replacement, 4): ['powerful', 'is', 'Spark', 'fast']
TakeOrdered (alphabetical, 5): ['Spark', 'Spark', 'Spark', 'easy', 'fast']
Top(5): ['use', 'to', 'powerful', 'is', 'is']
First element: Spark
IsEmpty?: False

Foreach output:
Word: Spark
Word: is
Word: fast
... (each word printed, order not guaranteed)

--- Aggregation Actions ---
Count: 11
CountByValue: {'Spark': 3, 'is': 3, 'fast': 1, 'powerful': 1, 'easy': 1, 'to': 1, 'use': 1}
Reduce (total word count): 11
Fold (total word count): 11
Aggregate (avg word length): 4.545454545454546
```

Note: Exact ordering (for `collect`, `takeSample`, etc.) may vary between runs because RDD operations are distributed and rely on partitioning.

## 🔍 Key Concepts

- Transformations are lazy (no execution until an action is called).
- Actions trigger computation and return results to the driver.
- `flatMap` is used to split each sentence into multiple words (1→N mapping).
- `map` transforms each element to a key-value tuple for grouping/aggregation.
- `reduceByKey` aggregates values for the same key efficiently by combining locally before shuffling.
- `aggregate` allows complex reductions with separate seq/comb functions (used here to compute average word length).

## 💡 Modifications to Try

- Change the input sentences in `exp3.py` to see how actions respond.
- Replace `words.foreach(lambda w: print(...))` with writing to a file using `saveAsTextFile` on a larger cluster.
- Use `map(lambda w: w.lower())` to make counting case-insensitive.
- Use `filter(lambda x: x.isalpha())` after removing punctuation to ignore punctuation tokens.

## 🐛 Troubleshooting

- "Cannot run multiple SparkContexts": Restart the Python session or the terminal. Only one SparkContext is allowed per JVM.
- Logging/`log4j` warnings: These are normal; the job will still run.
- If `pyspark` is missing: install it in your environment.

## 📚 Further Reading

- RDD Programming Guide: https://spark.apache.org/docs/latest/rdd-programming-guide.html
- PySpark RDD API: https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.RDD.html

---

**Experiment Level:** Beginner  
**Estimated Time:** 5–15 minutes
