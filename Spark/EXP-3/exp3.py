from pyspark import SparkContext
# Step 1: Initialize SparkContext
sc = SparkContext("local", "Basic RDD Transformations and Actions")
# Step 2: Create an RDD
data = ["Spark is fast", "Spark is powerful", "Spark is easy to use"]
rdd = sc.parallelize(data)
# Step 3: Transformations
words = rdd.flatMap(lambda line: line.split(" "))
word_pairs = words.map(lambda word: (word, 1))
word_count = word_pairs.reduceByKey(lambda a, b: a + b)
filtered_words = word_count.filter(lambda x: x[1] > 1)
# Step 4: Retrieval Actions
print("\n--- Retrieval Actions ---")
print("Collect:", words.collect())
print("Take(5):", words.take(5))
print("TakeSample (no replacement, 4):", words.takeSample(False, 4))
print("TakeOrdered (alphabetical, 5):", words.takeOrdered(5))
print("Top(5):", words.top(5))
print("First element:", words.first())
print("IsEmpty?:", words.isEmpty())
# foreach action (prints each word; order not guaranteed)
print("\nForeach output:")
words.foreach(lambda w: print("Word:", w))
# Step 5: Aggregation Actions
print("\n--- Aggregation Actions ---")
print("Count:", words.count())
print("CountByValue:", dict(words.countByValue()))
print("Reduce (total word count):", words.map(lambda x: 1).reduce(lambda a, b: a + b))
print("Fold (total word count):", words.map(lambda x: 1).fold(0, lambda a, b: a + b))
# Aggregate: Calculate average word length
agg_result = words.aggregate(
    (0, 0),  # (total length, word count)
    lambda acc, value: (acc[0] + len(value), acc[1] + 1),  # seqOp
    lambda acc1, acc2: (acc1[0] + acc2[0], acc1[1] + acc2[1])  # combOp
)
avg_word_length = agg_result[0] / agg_result[1]
print("Aggregate (avg word length):", avg_word_length)

# Step 6: Stop SparkContext
sc.stop()
