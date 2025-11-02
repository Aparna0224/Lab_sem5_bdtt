import findspark
findspark.init()

from pyspark import SparkConf, SparkContext

# Initialize SparkContext
conf = SparkConf().setAppName("PartitioningExample").setMaster("local[*]")
sc = SparkContext(conf=conf)

# Sample data
data = list(range(1, 21))  # Numbers from 1 to 20

# Create RDD with 4 partitions
rdd = sc.parallelize(data, 4)

print("Initial number of partitions:", rdd.getNumPartitions())

# Print elements in each partition
def inspect_partitions(index, iterator):
    yield f"Partition {index}: {list(iterator)}"

print("\nOriginal Partition Layout:")
for part in rdd.mapPartitionsWithIndex(inspect_partitions).collect():
    print(part)

# Repartition to 6 partitions (involves full shuffle)
rdd_repartitioned = rdd.repartition(6)
print("\nAfter repartition(6):")
print("Partitions:", rdd_repartitioned.getNumPartitions())
for part in rdd_repartitioned.mapPartitionsWithIndex(inspect_partitions).collect():
    print(part)

# Coalesce to 2 partitions (no full shuffle)
rdd_coalesced = rdd.coalesce(2)
print("\nAfter coalesce(2):")
print("Partitions:", rdd_coalesced.getNumPartitions())
for part in rdd_coalesced.mapPartitionsWithIndex(inspect_partitions).collect():
    print(part)

# Stop SparkContext
sc.stop()
