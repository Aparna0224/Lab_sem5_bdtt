# EXP-7: RDD Partitioning — repartition vs coalesce

## 📝 Description

This experiment demonstrates RDD partitioning behavior in PySpark. The script (`exp7.py`) creates an RDD of numbers, inspects how elements are distributed across partitions, then shows the difference between `repartition()` (full shuffle to increase/decrease partitions) and `coalesce()` (optimized, can avoid full shuffle when decreasing partitions).

## 🎯 Learning objectives

- Understand what partitions are and why they matter for parallelism
- See how to inspect partition layout with `mapPartitionsWithIndex`
- Learn when to use `repartition()` vs `coalesce()`
- Observe how data moves between partitions (shuffle vs no-shuffle)

## 📋 What the script does

1. Initializes a `SparkContext` with `local[*]` or similar.
2. Creates an RDD of numbers 1..20 with 4 partitions.
3. Prints the number of partitions and element lists per partition.
4. Calls `repartition(6)` and shows the new partition layout (involves a full shuffle).
5. Calls `coalesce(2)` on the original RDD and shows the new layout (no full shuffle by default).
6. Stops the SparkContext.

## ▶️ How to run

### Prerequisites

- Python 3.8+
- PySpark installed in your active environment (`pip install pyspark`) or run with `spark-submit` from a Spark distribution
- Java JDK 8 or 11 installed and `JAVA_HOME` set

### Run the script

From the project folder:

```bash
cd ~/projects/Big-Data-Spark/EXP-7
python exp7.py
```

Or with Spark's `spark-submit` (recommended for consistent environment):

```bash
$SPARK_HOME/bin/spark-submit --master local[*] exp7.py
```

## 📤 Expected output

You should see printed information similar to:

```
Initial number of partitions: 4

Original Partition Layout:
Partition 0: [1, 2, 3, 4, 5]
Partition 1: [6, 7, 8, 9]
Partition 2: [10, 11, 12, 13]
Partition 3: [14, 15, 16, 17, 18, 19, 20]

After repartition(6):
Partitions: 6
Partition 0: [..]
Partition 1: [..]
... (elements redistributed across 6 partitions)

After coalesce(2):
Partitions: 2
Partition 0: [..]
Partition 1: [..]
```

Note: exact partition contents may differ depending on Spark version and execution environment. `repartition()` will generally spread data more evenly because it shuffles; `coalesce()` will try to avoid shuffling and therefore may produce uneven partitions but is cheaper.

## 🔍 Key concepts

- Partitions: the unit of parallelism in Spark. More partitions → more parallel tasks (up to available cores).
- repartition(n): a shorthand for `coalesce(n, shuffle=True)`. Always does a full shuffle; use to increase or evenly redistribute partitions.
- coalesce(n): reduces partitions without a full shuffle by default (cheaper). Use when decreasing partitions and data skew is acceptable.
- Choosing the right number of partitions: typically 2–3 tasks per CPU core; tune to your cluster and job.

## 💡 Experiments to try

- Change the input size and see how partitioning affects task parallelism and runtime.
- Use `repartition()` to increase partitions before a heavy map stage to improve parallelism.
- Use `coalesce()` before writing output to reduce the number of output files cheaply.
- Try `coalesce(n, shuffle=True)` to force a shuffle while decreasing partitions (more even distribution).

## 🐛 Troubleshooting

- `ModuleNotFoundError: No module named 'pyspark'`: install with `pip install pyspark` or use `spark-submit`.
- `JAVA_HOME` not set / Java errors: install JDK and set `JAVA_HOME`.
- If output looks empty or partitions unexpected: remember that partitioning behavior can vary and RDD contents/order are not guaranteed; use `mapPartitionsWithIndex` as the script does to inspect partition contents.

## 📚 Further reading

- RDD Programming Guide: https://spark.apache.org/docs/latest/rdd-programming-guide.html
- Spark tuning guide (partitioning strategies): https://spark.apache.org/docs/latest/tuning.html

---

If you'd like, I can also:
- Add a short README section that explains how to measure timing between `repartition` and `coalesce` using `time` or Spark metrics, or
- Add a small test harness that runs the script and verifies partition counts. Which would you like?