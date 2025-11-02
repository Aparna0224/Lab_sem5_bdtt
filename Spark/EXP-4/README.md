# EXP-4: Distributed Sparse Matrix Multiplication

## 📝 Short description

This experiment demonstrates sparse matrix multiplication using Spark's distributed RDD API and the MLlib `CoordinateMatrix` representation. The repository contains a PySpark implementation (`exp4.py`) that performs multiplication by joining sparse matrix entries and summing partial products.

> Note: this folder previously contained a Scala example. A working PySpark version (`exp4.py`) is included so you can run it the same way as the other experiments.

## 🎯 What the script does

- Builds two sparse matrices A and B using `MatrixEntry(i, j, value)` entries stored in RDDs.
- Keys entries so A's columns match B's rows, performs an RDD join to compute pairwise products A[i,j] * B[j,k].
- Reduces by (i,k) to sum contributions and forms the resulting matrix entries.
- Wraps the result in a `CoordinateMatrix` and prints the non-zero entries.

This follows the classic distributed sparse-matrix multiplication approach (join on the shared dimension then reduce).

## Files

- `exp4.py` — PySpark implementation (ready to run)

## ✅ Prerequisites

- Java JDK 8 or 11 installed and `JAVA_HOME` set
- Python 3.8+
- PySpark installed (via `pip install pyspark` or using your project dependency manager)
- Optional: a local Spark installation to run with `spark-submit` (recommended for consistent behavior)

## ▶️ How to run

Run with the Python interpreter (works when `pyspark` is installed in the active environment):

```bash
cd ~/projects/Big-Data-Spark/EXP-4
python exp4.py
```

Or run with Spark's `spark-submit` (preferred if you have a Spark distribution):

```bash
# from WSL/bash
cd ~/projects/Big-Data-Spark/EXP-4
$SPARK_HOME/bin/spark-submit --master local exp4.py
```

If you see errors about missing `pyspark`, install it with:

```bash
pip install pyspark findspark
```

## 📤 Expected output

Given the hard-coded matrices in `exp4.py`, you should see the non-zero entries of the product matrix printed, e.g.:

```
(0,0) = 11.0
(0,1) = 14.0
(1,0) = 4.0
(1,1) = 6.0
```

Order may vary since RDD outputs aren't strictly ordered.

## ⚠️ Common issues & troubleshooting

- Error: `Not supported to call RDD.toDF before initialize SparkSession`
  - Fix: make sure `SparkSession` is created before any code that triggers `RDD.toDF()` (the current `exp4.py` already initializes `SparkSession`).

- Error: `ModuleNotFoundError: No module named 'pyspark'`
  - Fix: install PySpark in your active environment (`pip install pyspark`) or run with a Spark distribution's `spark-submit` which bundles the proper JARs.

- Error: Java not found or `JAVA_HOME` not set
  - Fix: install JDK and export `JAVA_HOME` (add to `~/.bashrc` or shell profile).

- Unexpected results or missing entries
  - Check that matrix indices are zero-based and entries are correct.
  - For large matrices, avoid `collect()`; write output to storage or use `saveAsTextFile`.

## Performance notes

- This join-and-reduce approach performs a shuffle on the join key and can be expensive for very large matrices. It's appropriate for sparse matrices but tune partitioning for large workloads.
- For production-scale jobs prefer optimized libraries or dedicated linear-algebra frameworks where possible.

## Scala version

- The original example in this repository used Scala/MLlib and performs the same algorithm. There is no rule that matrix-multiply must be implemented in Scala — both Scala and PySpark are valid. Scala may have slight performance benefits because it runs on the JVM natively, but PySpark is fully supported and convenient for scripting and learning.

## ✍️ Modifications & experiments to try

- Convert the code to use `mapPartitions` or custom partitioning to reduce shuffle overhead for larger inputs.
- Replace the hard-coded matrices with input readers (CSV or coordinate lists) to multiply arbitrary matrices.
- Add timing/logging to measure shuffle time and per-stage performance.

## 🧾 License / Notes

Educational example — intended for learning and small-scale experimentation.

---

If you want, I can also:
- Add an example that reads matrices from files (CSV / coordinate lists).
- Add a small unit test that verifies the computed entries.
Which would you prefer?