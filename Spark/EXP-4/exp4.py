from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.mllib.linalg.distributed import MatrixEntry, CoordinateMatrix

# Initialize SparkSession (CoordinateMatrix internally converts RDD -> DataFrame)
spark = SparkSession.builder.appName("PyMatrixMultiplyRDD").getOrCreate()
sc = spark.sparkContext

entriesA = sc.parallelize([
    MatrixEntry(0, 0, 1.0), MatrixEntry(0, 2, 2.0),
    MatrixEntry(1, 1, 3.0), MatrixEntry(1, 2, -1.0)
])
entriesB = sc.parallelize([
    MatrixEntry(0, 0, 1.0), MatrixEntry(1, 0, 3.0), MatrixEntry(2, 0, 5.0),
    MatrixEntry(0, 1, 2.0), MatrixEntry(1, 1, 4.0), MatrixEntry(2, 1, 6.0)
])

aKeyed = entriesA.map(lambda e: (e.j, (e.i, e.value)))
bKeyed = entriesB.map(lambda e: (e.i, (e.j, e.value)))

product = (aKeyed.join(bKeyed)
           .map(lambda kv: ((kv[1][0][0], kv[1][1][0]), kv[1][0][1] * kv[1][1][1]))
           .reduceByKey(lambda a, b: a + b)
           .map(lambda ik_sum: MatrixEntry(ik_sum[0][0], ik_sum[0][1], ik_sum[1])))

result = CoordinateMatrix(product)
for e in result.entries.collect():
    print(f"({e.i},{e.j}) = {e.value}")

spark.stop()