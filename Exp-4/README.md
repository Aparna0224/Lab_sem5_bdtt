# Experiment 4: Writing to Sequence Files in Hadoop

## Aim
To write key-value pairs into a Hadoop SequenceFile format and verify the content using Hadoop APIs.

## Concept
Hadoop SequenceFile is a binary file format used for storing key-value pairs in a Hadoop environment. It provides an efficient way to store data for MapReduce processing, supporting compression and serialization for Hadoop data types.

## Procedure

### Step 1: Verify Hadoop Environment
**Command:**
```bash
docker exec hadoop hadoop version
```
**Explanation:** Verifies that Hadoop is running in the Docker container.
**Expected Output:** Hadoop version information.

### Step 2: Compile the Java Program
**Command:**
```bash
docker cp Exp-4/SequenceFileWriterExample.java hadoop:/Exp-4/
docker exec hadoop bash -c "cd /Exp-4 && javac -classpath \$(hadoop classpath) SequenceFileWriterExample.java > compilation.log 2>&1"
```
**Explanation:** Copies the Java source to the container and compiles it, capturing any output to compilation.log.
**Compilation Log (compilation.log):**
```
(empty - successful compilation)
```

### Step 3: Create JAR Package
**Command:**
```bash
docker exec hadoop bash -c "cd /Exp-4 && jar cf seqwriter.jar SequenceFileWriterExample*.class"
```
**Explanation:** Packages the compiled classes into a JAR file.

### Step 4: Execute the Program
**Command:**
```bash
docker exec hadoop bash -c "cd /Exp-4 && hadoop jar seqwriter.jar SequenceFileWriterExample > execution_final.log 2>&1"
```
**Explanation:** Runs the program using hadoop jar command, logging output to execution_final.log.
**Execution Log (execution_final.log):**
```
2025-10-24 16:46:22,768 INFO sasl.SaslDataTransferClient: SASL encryption trust check: localHostTrusted = false, remoteHostTrusted = false
2025-10-24 16:46:24,123 INFO sasl.SaslDataTransferClient: SASL encryption trust check: localHostTrusted = false, remoteHostTrusted = false
2025-10-24 16:46:24,182 INFO zlib.ZlibFactory: Successfully loaded & initialized native-zlib library
2025-10-24 16:46:24,183 INFO compress.CodecPool: Got brand-new decompressor [.deflate]
Sequence file written successfully.
```

### Step 5: Verify File Creation
**Command:**
```bash
docker exec hadoop bash -c "cd /Exp-4 && ls -la sequencefile_output.seq"
```
**Explanation:** Checks that the sequencefile_output.seq was created locally.
**Output:**
```
-rw-r--r-- 1 root root 268 Oct 24 16:46 sequencefile_output.seq
```

### Step 6: Upload to HDFS
**Command:**
```bash
docker exec hadoop bash -c "cd /Exp-4 && hadoop fs -mkdir -p /user/hadoop && hadoop fs -put sequencefile_output.seq /user/hadoop/"
```
**Explanation:** Creates the HDFS directory and uploads the local sequence file to HDFS.

### Step 7: Verify Content in HDFS
**Command:**
```bash
docker exec hadoop bash -c "cd /Exp-4 && hadoop fs -text /user/hadoop/sequencefile_output.seq > verification_final.log 2>&1"
```
**Explanation:** Uses hadoop fs -text to read the binary SequenceFile and display content in readable format.
**Verification Log (verification_final.log):**
```
0	Value_0
1	Value_1
2	Value_2
3	Value_3
4	Value_4
```

## Result
Successfully wrote and verified data in Hadoop's SequenceFile format using Java API.

The experiment created a SequenceFile containing 5 key-value pairs (keys 0-4 with values "Value_0" to "Value_4"). The file was written to the local filesystem, uploaded to HDFS, and successfully read back using Hadoop's text command, confirming proper storage and retrieval of the serialized data.

**Notes:**
- The SequenceFileWriter was modified to explicitly write to the local filesystem by setting `fs.defaultFS` to `"file:///` in the Configuration to ensure compatibility with the standard procedure.
- All execution logs were captured throughout the process for debugging and verification purposes.
