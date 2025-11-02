from pyspark.sql import SparkSession
# Step 1: Create Spark session
spark = SparkSession.builder.appName("BasicSparkApp").getOrCreate()
# Step 2: Create DataFrame
data = [
    ("Alice", 22, "CSE"),
    ("Bob", 25, "ECE"),
    ("Charlie", 23, "CSE"),
    ("David", 21, "MECH")
]
columns = ["Name", "Age", "Department"]
df = spark.createDataFrame(data, columns)
# Step 3: Filter and select
result = df.filter(df.Department == "CSE").select("Name", "Age")
# Step 4: Display output
result.show()
# Stop Spark session
spark.stop()
