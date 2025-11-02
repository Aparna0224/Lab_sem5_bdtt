from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("WordCount").getOrCreate()
sc = spark.sparkContext

lines = sc.textFile("sample.txt")
words = lines.flatMap(lambda line: line.split())
wordPairs = words.map(lambda word: (word.lower(), 1))
wordCounts = wordPairs.reduceByKey(lambda a, b: a + b)
for word, count in wordCounts.collect():
    print(f"{word} {count}")

spark.stop()
