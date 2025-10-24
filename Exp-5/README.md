# Experiment 5: Implementing Map Side Join in MapReduce

## Aim
To implement a Map-Side Join using Hadoop MapReduce for joining a large dataset with a small lookup dataset using the Distributed Cache mechanism.

## Concept
A Map-Side Join is used when one dataset is small enough to fit into memory and the other dataset is large. The small dataset is distributed to all mappers using the DistributedCache or Hadoop's job.addCacheFile() method. Each mapper loads the small dataset into memory and performs the join operation locally as it processes records from the large dataset.

This approach improves performance by avoiding the shuffle and reduce phases, making it efficient for lookup-style joins.

## Prerequisites
- Hadoop 3.x running in Docker container
- Java 8 or higher installed in the environment
- Input datasets: customers.txt (small file) and orders.txt (large file)

## Dataset Overview
- **customers.txt**: Contains customer information in the format `C001,Customer1`, `C002,Customer2`, ..., up to 100 customers
- **orders.txt**: Contains order information in the format `O0001,C045,750`, `O0002,C012,200`, ..., total 450 orders with random customer IDs and amounts

## Procedure

### Step 1: Verify Hadoop Environment
**Command:**
```bash
docker exec hadoop hadoop version
```

**Explanation:** This command verifies that Hadoop is properly installed and running in the Docker container named "hadoop".

**Expected Output:**
Information about the Hadoop version and build details.

### Step 2: Create Input Directory in HDFS
**Command:**
```bash
docker exec hadoop hdfs dfs -mkdir -p /input
```

**Explanation:** Creates the `/input` directory in HDFS where we will store the dataset files.

**Expected Output:**
No errors reported, command completes successfully.

### Step 3: Upload Datasets to HDFS
**Command:**
```bash
docker exec hadoop hdfs dfs -put Exp-5/customers.txt /input/
docker exec hadoop hdfs dfs -put Exp-5/orders.txt /input/
```

**Explanation:** Copies the customers.txt and orders.txt files from the local filesystem to HDFS `/input` directory.

**Expected Output:**
Messages indicating successful file copy with SASL encryption checkpoints.

### Step 4: Compile the MapReduce Program
**Command:**
```bash
docker exec hadoop bash -c "cd /Exp-5 && javac -classpath \$(hadoop classpath) -d . MapSideJoinMapper.java MapSideJoinDriver.java"
```

**Explanation:** Compiles the Java source files using the Hadoop classpath, generating the corresponding .class files in the current directory.

**Expected Output:**
Compilation succeeds with a deprecation note (normal for older Hadoop versions).

### Step 5: Create JAR Package
**Command:**
```bash
docker exec hadoop bash -c "cd /Exp-5 && jar -cf mapjoin.jar MapSideJoin*.class"
```

**Explanation:** Packages the compiled class files into a JAR file named `mapjoin.jar` for distribution and execution.

**Expected Output:**
No output if successful, JAR file created.

### Step 6: Execute the MapReduce Job
**Command:**
```bash
docker exec hadoop bash -c "cd /Exp-5 && hadoop jar mapjoin.jar MapSideJoinDriver"
```

**Explanation:** Submits and runs the MapReduce job using the driver class. The job will:
- Load customers.txt into distributed cache
- Process orders.txt through the mapper
- Perform in-memory join between orders and customer data
- Output joined records

**Expected Output:**
Job submission information including job ID, localization of cache files, task progress, and final completion status.

### Step 7: View the Output
**Command:**
```bash
docker exec hadoop hdfs dfs -cat /output_mapjoin/part-m-00000
```

**Explanation:** Displays the contents of the mapper output file, showing the joined records sorted by order ID.

**Expected Output:**
Joined records in the format:
```
O0001    Customer45,750
O0002    Customer12,200
...
```

Each line contains the order ID as key, and customer name with order amount as value.

## Result
Map-side join was successfully implemented using the Distributed Cache. The join was performed in the Mapper, improving performance by avoiding the shuffle and reduce phases. The output shows each order with the corresponding customer name and order amount.

**Sample Output (first few lines):**
```
O0001    Customer45,750
O0002    Customer12,200
O0003    Customer78,340
...
```

This demonstrates the efficient processing of 450 orders joined with 100 customers using MapReduce's distributed cache mechanism.
