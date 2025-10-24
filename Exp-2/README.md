# Experiment 2: Processing Text Input with MapReduce

## Aim
To process a dataset of daily weather records and find the maximum temperature recorded for each year using MapReduce in Hadoop.

## Concept
MapReduce is a programming model for processing large datasets by dividing the work into smaller tasks (Map) that transform data and combine results (Reduce). This experiment demonstrates finding maximum values per group (year) by aggregating temperature data.

## Prerequisites
- Hadoop cluster running (DFS and YARN)
- Weather dataset (weather.csv)
- MapReduce classes compiled and packaged

## Dataset Overview
The experiment uses weather.csv with weather records:
```
Year,Month,Day,MaxTemperature,MinTemperature
2020,01,15,25,15
2020,02,20,32,18
2020,03,10,28,16
2020,04,05,30,20
2020,05,12,35,22
2021,01,10,22,12
2021,02,15,28,15
2021,03,20,31,19
2021,04,08,33,21
2021,05,18,36,24
2021,06,02,34,23
```

Expected maximum temperatures:
- 2020: 35° (maximum from 5 records)
- 2021: 36° (maximum from 6 records)

## Procedure

### Step 1: Upload Dataset to HDFS
```bash
docker cp Exp-2/weather.csv hadoop:/Exp-2/
docker exec hadoop hdfs dfs -put Exp-2/weather.csv /input/
```

**Expected Output:** Confirmation of file copy with SASL messages.

### Step 2: Compile Java Classes
```bash
docker exec hadoop bash -c "cd /Exp-2 && javac -classpath \$(hadoop classpath) -d . MaxTempMapper.java MaxTempReducer.java MaxTemperature.java"
```

**Expected Output:** Clean compilation (no errors).

### Step 3: Create JAR Package
```bash
docker exec hadoop bash -c "cd /Exp-2 && jar cf maxtemp.jar Max*.class"
```

**Expected Output:** JAR file created (size ~3KB).

### Step 4: Execute MapReduce Job
```bash
docker exec hadoop hadoop jar /Exp-2/maxtemp.jar MaxTemperature /input/weather.csv /output_maxtemp
```

**Expected Output:** Job completion messages.

### Step 5: View Results
```bash
docker exec hadoop hdfs dfs -cat /output_maxtemp/part-r-00000
```

**Expected Output:**
```
2020    35
2021    36
```

## Code Structure

### MaxTempMapper.java
- **Function:** Extracts year and max temperature from each line, skips header
- **Input:** (lineNumber, lineContent)
- **Output:** (year, maxTemperature)

### MaxTempReducer.java
- **Function:** Finds maximum temperature for each year
- **Input:** (year, [temp1, temp2, ...])
- **Output:** (year, maxTemperature)

### MaxTemperature.java (Driver)
- **Function:** Configures the MapReduce job
- **Components:** Sets mapper, reducer, combiner, input/output paths, key/value classes

## Result
Successfully processed weather data using MapReduce to find maximum temperature per year.

**Final Output:**
```
2020	35
2021	36
```

The experiment demonstrated:
- Data extraction and aggregation using MapReduce
- Year-based grouping and maximum finding
- Hadoop MapReduce job execution
- HDFS input/output handling

## Notes
- Uses combiner for optimized local aggregation
- Input format: CSV with header row
- Output sorted by year (natural sort)
