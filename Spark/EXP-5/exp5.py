from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("CreateDF").getOrCreate()
# From list of tuples
data = [("John", 28), ("Alice", 30), ("Bob", 25)]
df1 = spark.createDataFrame(data, ["name", "age"])
df1.show(); df1.printSchema()

# From RDD with schema
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
rdd = spark.sparkContext.parallelize([("John", 25), ("Mary", 30)])
schema = StructType([StructField("name", StringType(), True), StructField("age", IntegerType(), True)])
df2 = spark.createDataFrame(rdd.map(lambda x: (x[0], x[1])), schema)
df2.show(); df2.printSchema()

# From CSV
dfcsv = spark.read.csv("people.csv", header=True, inferSchema=True)
dfcsv.show(); dfcsv.printSchema()

df1.createOrReplaceTempView("people")
spark.sql("SELECT age, COUNT(*) AS cnt FROM people GROUP BY age").show()

spark.stop()
