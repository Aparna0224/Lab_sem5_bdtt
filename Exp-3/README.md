# Experiment 3: Running and Analyzing HIVE Queries on a Hadoop Cluster

## Aim
To create a table and run queries using Hive on a Hadoop cluster to analyze structured data stored in HDFS.

## Concept
Hive is a data warehouse software that facilitates reading, writing, and managing large datasets stored in distributed storage. It provides a SQL-like interface called HiveQL to query data, which gets translated into MapReduce jobs under the hood for analysis.

## Prerequisites
- Hadoop cluster running (DFS and YARN)
- Hive 3.x installed and configured
- Access to HDFS
- students.csv data file (provided)

## Dataset Overview
The experiment uses students.csv containing student information:
```
101,John,IT,85
102,Mary,CSE,90
103,Steve,ECE,78
```

Each record has:
- id: Student ID (integer)
- name: Student name (string)
- department: Department (string)
- marks: Marks scored (integer)

## Hive Installation (If Not Installed)

If Hive is not installed in your Hadoop environment, follow these steps:

### Step 1: Install wget in the container
```bash
docker exec -it -u root hadoop apt-get update
docker exec -it -u root hadoop apt-get install -y wget
```

### Step 2: Download Hive
```bash
docker exec -it -u root hadoop wget https://archive.apache.org/dist/hive/hive-3.1.3/apache-hive-3.1.3-bin.tar.gz
docker exec -it -u root hadoop tar -xzvf apache-hive-3.1.3-bin.tar.gz
docker exec -it -u root hadoop mv apache-hive-3.1.3-bin /usr/local/hive
```

### Step 3: Set Environment Variables
```bash
docker exec -it -u root hadoop bash -c 'echo "export HIVE_HOME=/usr/local/hive" >> ~/.bashrc'
docker exec -it -u root hadoop bash -c 'echo "export PATH=\$PATH:/usr/local/hive/bin" >> ~/.bashrc'
docker exec -it -u root hadoop source ~/.bashrc
```

### Step 4: Configure Hive-site.xml
```bash
docker exec -it -u root hadoop cp /usr/local/hive/conf/hive-default.xml.template /usr/local/hive/conf/hive-site.xml
```

### Step 5: Initialize Derby Metastore
```bash
docker exec hadoop /usr/local/hive/bin/schematool -dbType derby -initSchema
```

**Note:** If package installation fails due to network issues, a Hive-enabled Docker image (e.g., bde2020/hadoop-hive:2.0.0-hive2.3.2) may be preferred.

## Procedure

### Step 1: Start Hadoop Services
```bash
docker exec hadoop start-dfs.sh
docker exec hadoop start-yarn.sh
```

**Expected Output:** Success messages for starting DFS and YARN services.

### Step 2: Upload Input Data to HDFS
```bash
docker exec hadoop hdfs dfs -mkdir -p /user/hive/input
docker exec hadoop hdfs dfs -put Exp-3/students.csv /user/hive/input/
```

**Expected Output:** Confirmation of directory creation and file upload.

### Step 3: Start Hive CLI
```bash
docker exec -it hadoop hive
```

**Expected Output:** Enters Hive CLI shell prompt.

### Step 4: Create Database
```sql
CREATE DATABASE studentdb;
```

**Expected Output:**
```
OK
Time taken: 0.234 seconds
```

### Step 5: Use Database and Create Table
```sql
USE studentdb;

CREATE TABLE students (
    id INT,
    name STRING,
    department STRING,
    marks INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE;
```

**Expected Output:**
```
OK
Time taken: 0.145 seconds
```

### Step 6: Load Data into Table
```sql
LOAD DATA INPATH '/user/hive/input/students.csv' INTO TABLE students;
```

**Expected Output:**
```
Loading data to table studentdb.students
Table studentdb.students stats: [numFiles=1, totalSize=60]
OK
Time taken: 2.123 seconds
```

### Step 7: Query Operations

#### Query 1: View All Records
```sql
SELECT * FROM students;
```

**Expected Output:**
```
OK
101	John	IT	85
102	Mary	CSE	90
103	Steve	ECE	78
Time taken: 0.234 seconds, Fetched: 3 row(s)
```

#### Query 2: Students with Marks > 80
```sql
SELECT name, department FROM students WHERE marks > 80;
```

**Expected Output:**
```
OK
John	IT
Mary	CSE
Time taken: 0.123 seconds, Fetched: 2 row(s)
```

#### Query 3: Count Total Students
```sql
SELECT COUNT(*) FROM students;
```

**Expected Output:**
```
OK
3
Time taken: 0.087 seconds, Fetched: 1 row(s)
```

### Step 8: Exit Hive CLI
```sql
exit;
```

## Result
Hive queries were successfully executed on a Hadoop cluster. The student data was analyzed using HiveQL, demonstrating Hive's ability to perform SQL-like operations over data stored in HDFS.

The queries provided insights into:
- Complete student records
- High-performing students (marks > 80)
- Total student count

This experiment showcases the power of Hive for structured data analysis in the Big Data ecosystem.

## Notes
- If networking issues prevent installation, consider using a pre-built Docker image with Hive
- The experiment assumes Hadoop services are operational
- All commands should be executed within the Hadoop Docker container environment
