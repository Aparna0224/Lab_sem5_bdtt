# Big Data Laboratory Experiments (Semester 5)

## Overview
This repository contains comprehensive Hadoop and Big Data experiments demonstrating various MapReduce programming patterns, SQL-like data querying with Hive, file system operations, and distributed data processing techniques. All experiments are designed to run in a Dockerized Hadoop environment for easy setup and consistent execution.

## Experiments Index

### Exp-1: Hadoop WordCount with Combiner
**Description:** Demonstrates the classic WordCount MapReduce job with a Combiner optimization for efficiency in reducing intermediate data transfer. Shows how to compile, package, and execute Java MapReduce programs in a Docker container.

**Key Concepts:**
- MapReduce programming model
- Combiner for optimization
- Docker volume mounting
- HDFS operations

**File Location:** `Exp-1/`

### Exp-2: Processing Text Input with MapReduce
**Description:** Processes weather data records to find maximum temperatures per year using custom MapReduce jobs. Demonstrates data aggregation and group-by operations in MapReduce.

**Key Concepts:**
- Custom Mapper and Reducer classes
- Data aggregation by key
- Max value calculation
- CSV text processing

**File Location:** `Exp-2/`

**Output:**
```
2020	35
2021	36
```

### Exp-3: Analyzing Hive Queries on Hadoop Cluster
**Description:** Creates a Hive database and table to run SQL-like queries on student data. Demonstrates Hive setup, table creation, data loading, and querying structured data stored in HDFS.

**Key Concepts:**
- Hive database operations
- Table schema definition
- Data loading from HDFS
- HiveQL queries (SELECT, WHERE, COUNT)

**File Location:** `Exp-3/`

Note: Requires manual Hive installation in the Docker container.

### Exp-4: Writing to Sequence Files in Hadoop
**Description:** Creates and reads Hadoop SequenceFile format, demonstrating binary file operations for MapReduce data storage. Shows efficient serialization of key-value pairs.

**Key Concepts:**
- SequenceFile creation and reading
- Hadoop file system operations
- Binary data formats
- BufferedReader and DistributedCache

**File Location:** `Exp-4/`

**Output:**
```
0	Value_0
1	Value_1
2	Value_2
3	Value_3
4	Value_4
```

### Exp-5: Implementing Map Side Join in MapReduce
**Description:** Performs efficient map-side joins between large and small datasets using DistributedCache. Optimizes join operations by avoiding reduce phase shuffle.

**Key Concepts:**
- Map-side join performance optimization
- DistributedCache for small datasets
- In-memory join operations
- Key-value pair matching

**File Location:** `Exp-5/`

## Prerequisites

### System Requirements
- **Operating System:** Linux/MacOS/Windows with WSL (Ubuntu recommended)
- **Docker:** Installed and running with sufficient resources
- **Java:** JDK 8 or higher (included in Hadoop container)
- **Git:** For cloning the repository

### Hadoop Environment
- **Docker Image:** `ronnieallen/myhadoop` (customized Hadoop container)
- **Hadoop Version:** 3.2.1
- **Ports Required:**
  - 9000 (HDFS NameNode)
  - 9870 (YARN Resource Manager)
  - 9864 (DataNode)
  - 8088 (Job History)

### Network Requirements
- Internet access for downloading Docker images
- Localhost port availability for Hadoop web interfaces

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Aparna0224/Lab_sem5_bdtt.git
cd Lab_sem5_bdtt
```

### 2. Start Hadoop Container
```bash
docker run -d --name hadoop \
  -p 9000:9000 -p 9870:9870 -p 9864:9864 -p 8088:8088 \
  -v hadoop_namenode:/hadoop/dfs/name \
  -v hadoop_datanode:/hadoop/dfs/data \
  -v $(pwd):/localfiles \
  ronnieallen/myhadoop
```

### 3. Verify Setup
```bash
docker exec hadoop jps
```

Expected output should show HDFS and YARN processes.

### 4. Run Experiments
Each experiment directory contains detailed README.md files with step-by-step instructions:

```bash
# Navigate to experiment directory
cd Exp-2

# Follow the README.md instructions
```

## Results Summary

| Experiment | Input | Output | Target |
|------------|-------|--------|--------|
| Exp-1 | Text file | Word counts | [java:3 hadoop:1 ...] |
| Exp-2 | Weather CSV | Max temp/year | 2020:35, 2021:36 |
| Exp-3 | Student CSV | Query results | SELECT * showing student records |
| Exp-4 | N/A | Sequence file | 5 key-value pairs |
| Exp-5 | Customer/Orders | Joined records | Customer names + amounts |

## Docker and Hadoop Commands Reference

### Docker Operations
```bash
# Execute commands in container
docker exec -it hadoop bash

# Copy files between host and container
docker cp Exp-2/weather.csv hadoop:/Exp-2/

# View container logs
docker logs hadoop
```

### HDFS Operations
```bash
# Create directories
hdfs dfs -mkdir -p /input

# Upload files
hdfs dfs -put filename.txt /input/

# List files
hdfs dfs -ls /input

# View file contents
hdfs dfs -cat /output/part-r-00000

# Remove directories
hdfs dfs -rm -r /output
```

### Hadoop Job Execution
```bash
# Run MapReduce job
hadoop jar program.jar DriverClass input_path output_path

# Check job status
hdfs dfs -ls /
```

## Troubleshooting

### Common Issues
1. **Port conflicts:** Stop conflicting services or change ports
2. **Permission issues:** Ensure Docker runs with proper privileges
3. **Memory errors:** Increase Docker resources if needed
4. **Compilation fails:** Verify Java classpath and syntax
5. **Job doesn't start:** Check HDFS formats and YARN services

### Web Interfaces
- **Hadoop NameNode:** http://localhost:9870
- **YARN Resource Manager:** http://localhost:8088
- **DataNode:** http://localhost:9864

### Health Checks
```bash
# Check Hadoop processes
docker exec hadoop jps

# Test HDFS
docker exec hadoop hdfs dfs -ls /

# Test YARN application status
docker exec hadoop yarn application -list
```

## Learning Outcomes

By completing these experiments, you'll understand:

- **MapReduce Programming:** Core patterns (word count, aggregation, joins)
- **Hadoop Ecosystem:** HDFS storage, YARN resource management
- **Big Data Processing:** Distributed computation, data serialization
- **Optimization Techniques:** Combiners, distributed caches, sequence files
- **SQL-like Operations:** Hive queries for structured data analysis
- **Containerization:** Running complex Big Data stacks in Docker

## Repository Information

- **GitHub:** https://github.com/Aparna0224/Lab_sem5_bdtt
- **Last Commit:** `e0051984026fcab9cf7989425434856001761ba1`
- **Environment:** Laboratory coursework for Big Data semester 5

## Contributing

This is an educational repository for Big Data laboratory work. Each experiment is self-contained with detailed documentation for reproducibility.

---

*Built with Hadoop 3.2.1, Java 8, and Docker containerization*
