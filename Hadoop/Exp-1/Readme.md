# Experiment 1: Hadoop WordCount with Combiner

## Aim
To implement a Hadoop MapReduce WordCount job with a Combiner to demonstrate efficient word frequency counting and intermediate data optimization.

## Concept
MapReduce is a programming model for processing large datasets with a parallel distributed algorithm. WordCount is the classic "Hello World" of MapReduce, counting word occurrences in text. A Combiner acts as a mini-reducer on the mapper node, reducing intermediate key-value pairs before shuffle/sort phase, improving performance by minimizing data transfer to reducers.

## Prerequisites
- Hadoop 3.x running in Docker container
- Java 8 or higher installed in the environment
- Input dataset: input.txt (text file)

## Dataset Overview
The experiment uses input.txt with the text: "hello hadoop hello docker hello world"

Expected to produce word counts showing frequency of each unique word.

## Procedure

### Step 1: Copy Experiment Files to Hadoop Container
**Command:**
```bash
docker cp Exp-1 hadoop:/Exp-1
```
**Explanation:** Copies the Exp-1 directory containing Java source files and dataset from host to the running Hadoop Docker container.
**Expected Output:**
```
Successfully copied 16.9kB to hadoop:/Exp-1
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

### Step 3: Compile Java Classes
**Command:**
```bash
docker exec hadoop bash -c "cd /Exp-1 && javac -classpath \$(hadoop classpath) -d . WC_Mapper.java WC_Reducer.java WC_Driver.java"
```
**Explanation:** Compiles the Java source files using the Hadoop classpath, generating the corresponding .class files in the current directory.
**Expected Output:**
Clean compilation with no errors.

### Step 4: Create JAR Package
**Command:**
```bash
docker exec hadoop bash -c "cd /Exp-1 && jar cf wordcount-combiner.jar WC*.class"
```
**Explanation:** Packages the compiled class files into a JAR file named wordcount-combiner.jar for distribution and execution.
**Expected Output:**
JAR file created successfully.

### Step 5: Upload Dataset to HDFS
**Command:**
```bash
docker exec hadoop hdfs dfs -mkdir -p /input
docker exec hadoop hdfs dfs -put /Exp-1/input.txt /input/
```
**Explanation:** Creates the /input directory in HDFS and uploads the input.txt file from the container's local filesystem to HDFS.
**Expected Output:**
SASL encryption trust check message and confirmation of successful file transfer.

### Step 6: Execute MapReduce Job
**Command:**
```bash
docker exec hadoop hadoop jar /Exp-1/wordcount-combiner.jar WC_Driver /input/input.txt /output_wordcount
```
**Explanation:** Runs the WordCount MapReduce job with combiner, processing input.txt and storing results in /output_wordcount directory.
**Expected Output:**
Job submission logs showing map and reduce tasks completion, counters indicating combiner effectiveness (Combine input records=6, Combine output records=4), and final job success message.

### Step 7: View Results
**Command:**
```bash
docker exec hadoop hdfs dfs -cat /output_wordcount/part-r-00000
```
**Explanation:** Displays the contents of the output file, showing the word count results sorted by word.
**Expected Output:**
```
docker	1
hadoop	1
hello	3
world	1
```

## Code Structure

### WC_Mapper.java
- **Function:** Reads text input line by line, tokenizes into words, emits each word with count 1
- **Input:** (line_offset, line_content)
- **Output:** (word, 1)

### WC_Reducer.java
- **Function:** Aggregates word counts from mapper outputs (and combiner), used both as reducer and combiner
- **Input:** (word, [count1, count2, ...])
- **Output:** (word, total_count)

### WC_Driver.java (Driver)
- **Function:** Configures the MapReduce job with input/output paths, mapper/reducer classes, combiner class, and job settings
- **Components:** Sets input format (TextInputFormat), output format (TextOutputFormat), key/value types (Text/IntWritable)

## Result
Successfully executed WordCount MapReduce job with combiner optimization. The combiner reduced intermediate data transfer by aggregating locally on mapper nodes.

**Sample Output:**
```
docker	1
hadoop	1  
hello	3
world	1
```

The experiment demonstrates:
- Basic MapReduce word counting functionality
- Combiner usage for performance optimization (6 mapper outputs reduced to 4 combiner outputs)
- Hadoop MapReduce job configuration and execution
- HDFS input/output handling

## Notes
- Combiner serves as local reducer on mapper nodes, reducing network traffic
- Job counters show combiner effectiveness: Combine input records=6, Combine output records=4
- Uses Hadoop's distributed file system for input/output
- Single-node setup suitable for learning and small-scale processing
