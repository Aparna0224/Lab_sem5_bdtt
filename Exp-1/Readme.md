# 🧩 Hadoop WordCount with Combiner — Docker Setup

This project demonstrates running a Hadoop MapReduce WordCount job with a Combiner inside a Docker container.
The Combiner reduces intermediate data transferred between Mapper and Reducer, improving job efficiency.

## 🔧 1️⃣ Prerequisites

Before starting, ensure the following:

- **Docker installed** on your host machine
  - Docker allows you to run Hadoop inside an isolated container without installing it directly on your host OS.

- **Hadoop Docker image**: `ronnieallen/myhadoop`
  - Pre-installed with:
    - **Hadoop 3.2.1** — distributed computing framework
    - **Java JDK 1.8** — required to compile and run MapReduce jobs

- **Basic understanding** of HDFS (Hadoop Distributed File System) and MapReduce programming

## 📂 2️⃣ Project Structure on Host

Organize your project files like this:

```
~/Documents/hadoop_lab/
├─ data/
│  ├─ WC_Mapper.java       # Mapper class
│  ├─ WC_Reducer.java      # Reducer & Combiner class
│  ├─ WC_Driver.java       # Driver class
├─ input.txt               # Sample input text file
```

- **Mapper class** (`WC_Mapper.java`): Reads input data line by line and emits intermediate key-value pairs.
- **Reducer class** (`WC_Reducer.java`): Aggregates intermediate results; optionally acts as a combiner to reduce network traffic.
- **Driver class** (`WC_Driver.java`): Configures and submits the MapReduce job.

The `data/` folder will also store compiled `.class` files and the final `.jar` file.

## 💡 3️⃣ Key Concepts

### 3.1 pwd
- **Stands for** Print Working Directory
- **Shows** the full path of the current directory in the terminal
- **Useful** to confirm your current path before mounting it to Docker

**Example:**
```bash
pwd
# Output: /home/aparna/Documents/hadoop_lab
```

### 3.2 Classpath
The classpath is a list of directories and JAR files that Java uses to locate classes and libraries.
Hadoop programs depend on Hadoop libraries; if missing, compilation or execution will fail.

**Example:**
```bash
javac -cp `hadoop classpath` WC_Mapper.java
```

The command `hadoop classpath` outputs all Hadoop library paths needed for compiling MapReduce code.

### 3.3 JAR File
A Java Archive (JAR) packages compiled `.class` files and resources into a single executable file.

Hadoop expects a single JAR containing all Mapper, Reducer, and Driver classes.

**Example:**
```bash
jar -cvf wordcount-combiner.jar -C wc_classes/ .
```

**Flags:**
- `-c` → Create archive
- `-v` → Verbose output
- `-f` → Specify filename
- `-C wc_classes/ .` → Include all compiled `.class` files

### 3.4 Docker Volume Mount (-v)
Maps a directory on the host machine to a directory inside the Docker container.

**Why external volume is required:**
- Ensures persistent storage for Hadoop NameNode & DataNode data
- Allows shared access between host and container
- Enables retrieving output and JAR files without copying manually

**Example:**
```bash
-v hadoop_namenode:/hadoop/dfs/name
-v hadoop_datanode:/hadoop/dfs/data
-v $(pwd):/localfiles
```

## 🧠 4️⃣ Java Source Code

### WC_Driver.java
```java
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class WC_Driver {
    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            System.err.println("Usage: WC_Driver <input> <output>");
            System.exit(2);
        }
        Job job = Job.getInstance(new Configuration(), "Word Count with Combiner");
        job.setJarByClass(WC_Driver.class);
        job.setMapperClass(WC_Mapper.class);
        job.setCombinerClass(WC_Reducer.class);
        job.setReducerClass(WC_Reducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
```

### WC_Mapper.java
```java
import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class WC_Mapper extends Mapper<LongWritable, Text, Text, IntWritable> {
    private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();

    @Override
    protected void map(LongWritable key, Text value, Context context)
        throws IOException, InterruptedException {
        StringTokenizer itr = new StringTokenizer(value.toString());
        while (itr.hasMoreTokens()) {
            word.set(itr.nextToken());
            context.write(word, one);
        }
    }
}
```

### WC_Reducer.java
```java
import java.io.IOException;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class WC_Reducer extends Reducer<Text, IntWritable, Text, IntWritable> {
    private IntWritable result = new IntWritable();

    @Override
    protected void reduce(Text key, Iterable<IntWritable> values, Context context)
        throws IOException, InterruptedException {
        int sum = 0;
        for (IntWritable val : values) {
            sum += val.get();
        }
        result.set(sum);
        context.write(key, result);
    }
}
```

## ⚙️ 5️⃣ Steps to Run WordCount in Dockerized Hadoop

### 📁 Step 1: Set Up the Hadoop Lab Directory
```bash
cd Documents
mkdir hadoop_lab
cd hadoop_lab
```

Inside the `hadoop_lab` directory, create a `data` folder:
```bash
mkdir data
```

Add your Java files (`WC_Mapper.java`, `WC_Reducer.java`, `WC_Driver.java`) into the `data` folder.
These files will be mounted into the Docker container to compile and execute your WordCount program.

After adding your Java files:
```bash
cd ..
```

### 🐳 Step 2: Pull and Run the Hadoop Docker Container
```bash
docker pull ronnieallen/myhadoop
docker run -d --name hadoop \
  -p 9870:9870 -p 9000:9000 -p 9864:9864 \
  -v hadoop_namenode:/hadoop/dfs/name \
  -v hadoop_datanode:/hadoop/dfs/data \
  -v $(pwd)/hadoop_lab:/localfiles \
  ronnieallen/myhadoop
```

### 🖥️ Step 3: Access the Hadoop Container
```bash
docker exec -it hadoop bash
hdfs dfs -mkdir /exp_1
hdfs dfs -put /localfiles/data/* /exp_1/
```

### ☕ Step 4: Compile and Package the Java Files
```bash
cd /localfiles/data
mkdir -p wc_classes
javac -cp `hadoop classpath' -d wc_classes WC_Mapper.java WC_Reducer.java WC_Driver.java
jar -cvf wordcount-combiner.jar -C wc_classes/ .
echo "hello hadoop hello docker hello world" > input.txt
```

### 📂 Step 5: Prepare Input and Run the WordCount Job
```bash
hdfs dfs -mkdir -p /wordcount/input
hdfs dfs -put input.txt /wordcount/input
hdfs dfs -ls /wordcount/input
hadoop jar /localfiles/data/wordcount-combiner.jar WC_Driver /wordcount/input /wordcount/output
hdfs dfs -cat /wordcount/output/part-r-00000
```

### ✅ Step 6: Clean Up
```bash
docker stop hadoop
docker rm hadoop
```

## 📌 Notes

- Ensure Docker is installed and running on your system.
- The image `ronnieallen/myhadoop` provides a single-node Hadoop setup.
- The Java files implement a standard MapReduce WordCount job with a Combiner for optimization.

## 🎯 Expected Output

After running the WordCount job, you should see output similar to:
```
docker  1
hadoop  1
hello   3
world   1
```

This shows the word count for each unique word in the input text, demonstrating that the Combiner successfully reduced intermediate data before sending it to the Reducer.

## 🔧 Troubleshooting

### Common Issues:
1. **Docker not found**: Ensure Docker is installed and the Docker daemon is running
2. **Permission denied**: Check that your user has permission to run Docker commands
3. **Port conflicts**: Make sure ports 9870, 9000, and 9864 are not already in use
4. **Java compilation errors**: Verify that all Java files are in the correct directory and have proper syntax

### Useful Commands:
```bash
# Check Docker status
docker ps -a

# View Hadoop logs
docker logs hadoop

# Access Hadoop Web UI
http://localhost:9870
```
