# Experiment 5: Implementing Map Side Join in MapReduce

## Aim
To implement a Map-Side Join using Hadoop MapReduce for joining a large dataset with a small lookup dataset using the Distributed Cache mechanism.

## Concept
Map-Side Join is used when one dataset is small enough to fit into memory and the other is large. The small dataset is distributed to all mappers using the DistributedCache or Hadoop's job.addCacheFile() method. Each mapper loads the small dataset into memory and performs the join operation locally as it processes records from the large dataset. This approach improves performance by avoiding the shuffle and reduce phases, making it efficient for lookup-style joins where no aggregation is needed.

## Prerequisites
- Hadoop 3.x running in Docker container
- Java 8 or higher installed in the environment
- Input datasets: customers.txt (small file) and orders.txt (large file)

## Dataset Overview
- **customers.txt**: Contains customer information in the format `C001,Customer1`, `C002,Customer2`, ..., up to 100 customers (small lookup dataset)
- **orders.txt**: Contains order information in the format `O0001,C045,750`, `O0002,C012,200`, ..., total 450 orders with random customer IDs and amounts (large dataset to be joined)

## Procedure

### Step 1: Copy Experiment Files to Hadoop Container
**Command:**
```bash
docker cp Exp-5 hadoop:/Exp-5
```
**Explanation:** Copies the Exp-5 directory containing Java source files and datasets from host to the running Hadoop Docker container.
**Expected Output:**
```
Successfully copied 21kB to hadoop:/Exp-5
```

### Step 2: Verify Hadoop Environment
**Command:**
```bash
docker exec hadoop hadoop version
```
**Explanation:** Verifies that Hadoop is properly installed and running in the Docker container named "hadoop".
**Expected Output:**
```
Hadoop 3.2.1
Source code repository https://gitbox.apache.org/repos/asf/hadoop.git -r b3cbbb467e22ea829b3808f4b7b01d07e0bf3842
Compiled by rohithsharmaks on 2019-09-10T15:56Z
Compiled with protoc 2.5.0
From source with checksum 776eaf9eee9c0ffc370bcbc1888737
This command was run using /opt/hadoop-3.2.1/share/hadoop/common/hadoop-common-3.2.1.jar
```

### Step 3: Create Input Directory in HDFS
**Command:**
```bash
docker exec hadoop hdfs dfs -mkdir -p /input
```
**Explanation:** Creates the `/input` directory in HDFS where we will store the dataset files.
**Expected Output:**
Creates directory successfully without errors.

### Step 4: Upload Datasets to HDFS
**Command:**
```bash
docker exec hadoop hdfs dfs -put Exp-5/customers.txt /input/
docker exec hadoop hdfs dfs -put Exp-5/orders.txt /input/
```
**Explanation:** Copies the customers.txt and orders.txt files from the container's local filesystem to HDFS `/input` directory.
**Expected Output:**
SASL encryption trust check messages confirming successful file transfers.

### Step 5: Compile the MapReduce Program
**Command:**
```bash
docker exec hadoop bash -c "cd /Exp-5 && javac -classpath \$(hadoop classpath) -d . MapSideJoinMapper.java MapSideJoinDriver.java"
```
**Explanation:** Compiles the Java source files using the Hadoop classpath, generating the corresponding .class files in the current directory.
**Expected Output:**
Compilation succeeds (may show deprecation note for MapSideJoinMapper.java, normal for older Hadoop API usage).

### Step 6: Create JAR Package
**Command:**
```bash
docker exec hadoop bash -c "cd /Exp-5 && jar -cf mapjoin.jar MapSideJoin*.class"
```
**Explanation:** Packages the compiled class files into a JAR file named mapjoin.jar for distribution and execution.
**Expected Output:**
JAR file created successfully.

### Step 7: Execute the MapReduce Job
**Command:**
```bash
docker exec hadoop bash -c "cd /Exp-5 && hadoop jar mapjoin.jar MapSideJoinDriver"
```
**Explanation:** Submits and runs the MapReduce job using the driver class. The job loads customers.txt into distributed cache, processes orders.txt through the mapper, performs in-memory join between orders and customer data, and outputs joined records.
**Expected Output:**
Job submission logs showing distributed cache localization (customers.txt), task progress with 450 map input records and 450 map output records, and final job success with map 100% reduce 0% (indicating map-side join with no reducer).

### Step 8: View the Output
**Command:**
```bash
docker exec hadoop hdfs dfs -cat /output_mapjoin/part-m-00000
```
**Explanation:** Displays the contents of the mapper output file, showing all 450 joined records sorted by order ID.
**Expected Output:**
450 lines of joined records in the format:
```
O0001	Customer16,9565
O0002	Customer59,3277
O0003	Customer84,2815
...
O0450	Customer12,3006
```

Each line contains the order ID as key (tab-separated) and customer name with order amount as value.

## Code Structure

### MapSideJoinMapper.java
- **Function:** Loads customers.txt into memory via distributed cache during setup phase, processes each order from orders.txt, looks up customer name by ID, emits (orderID, customerName+","+orderAmount) pairs
- **Input:** (line_offset, order_line)
- **Output:** (orderID, joined_record)

### MapSideJoinDriver.java (Driver)
- **Function:** Configures the MapReduce job with no reducer (job.setNumReduceTasks(0)), adds customers.txt to distributed cache, sets input paths and output format
- **Key Configuration:** Uses DistributedCache.addCacheFile() for lookup dataset, sets FileInputFormat for orders.txt

## Result
Map-side join was successfully implemented using the Distributed Cache. The join was performed entirely in the Mapper without a reducer, improving performance by avoiding the shuffle phase. The job processed 450 orders and joined each with the corresponding customer information from the 100-customer lookup dataset.

**Sample Output (first 10 lines):**
```
O0001	Customer16,9565
O0002	Customer59,3277
O0003	Customer84,2815
O0004	Customer50,361
O0005	Customer53,9127
O0006	Customer22,1999
O0007	Customer99,302
O0008	Customer22,2459
O0009	Customer89,4150
O0010	Customer4,4854
```

The experiment demonstrates:
- Effective map-side join using distributed cache for small dataset distribution
- No shuffle/sort phase (reduce 0% in job counters)
- Processing of 450 join operations efficiently in the mapper phase
- Output sorted by order ID (natural key sort)

## Notes
- Distributed cache enables efficient lookup without reducer phase
- Small dataset (customers.txt) fits in memory for in-mapper joining
- Job counters show 450 map input/output records with no spill or shuffle operations
- Deprecated API usage in mapper is normal for Hadoop 3.x backward compatibility
- Suitable for star-schema joins or lookup enrichment operations
