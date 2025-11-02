from pyspark import SparkContext
from pyspark.streaming import StreamingContext
# Step 1: Initialize SparkContext and StreamingContext with 5-second batch interval
sc = SparkContext("local[2]", "NetworkWordCount")
ssc = StreamingContext(sc, 5)
# Step 2: Create a DStream that connects to localhost:9999
lines = ssc.socketTextStream("localhost", 9999)
# Step 3: Split each line into words
words = lines.flatMap(lambda line: line.split(" "))
# Step 4: Count each word in each batch
pairs = words.map(lambda word: (word, 1))
wordCounts = pairs.reduceByKey(lambda x, y: x + y)
# Step 5: Print the result
wordCounts.pprint()
# Step 6: Start the streaming computation
ssc.start()
# Step 7: Wait for the computation to terminate
ssc.awaitTermination()
