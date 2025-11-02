# EXP-6: Spark Streaming — Network Word Count

## 📝 Description

This experiment demonstrates a simple Spark Streaming job that connects to a TCP socket (localhost:9999), reads text lines in micro-batches, splits them into words, and prints word counts for each batch. It uses PySpark's DStream API (classic Spark Streaming).

## 🎯 Learning objectives

- Learn how to create a StreamingContext and process DStreams
- Understand micro-batching (batch interval) and streaming execution flow
- Practice feeding data to a streaming job via a TCP socket (netcat)
- Observe transformation (`flatMap`, `map`, `reduceByKey`) and action (`pprint`) on DStreams

## 📁 Files

- `exp6.py` — streaming program that connects to `localhost:9999` and prints word counts every 5 seconds

## ✅ Prerequisites

- Python 3.8+
- PySpark installed in your active environment (`pip install pyspark`) or a full Spark distribution (use `spark-submit`)
- Java JDK 8 or 11 installed and `JAVA_HOME` set
- `nc` (netcat) available in WSL to act as a streaming data source (or an alternative sender)

## ▶️ How to run

You must run two terminals:

1) Start the data source (netcat) — Terminal A
2) Run the Spark streaming job — Terminal B

### Terminal A — start netcat (WSL recommended)

```bash
# simple persistent listener (recommended if netcat supports -k)
nc -lk 9999

# If your netcat doesn't support -k, keep it in a loop:
while true; do nc -l 9999; done
```

Type lines in that terminal and press Enter — those lines will be picked up by the Spark job.

If `nc` is not installed:

```bash
sudo apt update
sudo apt install netcat-openbsd
```

### Terminal B — run the Spark Streaming job

Preferred (uses your Spark distribution):

```bash
cd ~/projects/Big-Data-Spark/EXP-6
$SPARK_HOME/bin/spark-submit --master local[2] exp6.py
```

Or run with the Python interpreter if `pyspark` is installed in your virtualenv:

```bash
cd ~/projects/Big-Data-Spark/EXP-6
python exp6.py
```

Notes:
- Use `local[2]` (or more cores) for streaming so Spark has resources for the receiver and processing.
- The script uses a 5-second batch interval; you will see counts emitted every 5 seconds.

## 📤 Expected output

When you type text into the netcat terminal, the Spark job prints counts for the current batch. Example (format varies slightly):

```
-------------------------------------------
Time: 2025-11-02 12:00:05
-------------------------------------------
('hello', 1)
('spark', 2)
('streaming', 1)
```

Each printed block corresponds to a 5-second micro-batch.

## 🔧 Common issues & fixes

- "ModuleNotFoundError: No module named 'pyspark'"
  - Install PySpark into your environment: `pip install pyspark findspark`
  - Or run with Spark's `spark-submit` which supplies Spark jars.

- "JAVA_HOME is not set" / Java errors
  - Install JDK and set `JAVA_HOME` (for WSL/Ubuntu):

```bash
sudo apt update && sudo apt install openjdk-11-jdk
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
```

- "Connection refused" when Spark tries to connect to localhost:9999
  - Make sure netcat is running and listening on the same port.
  - Firewalls or binding to different interfaces may cause issues — use WSL to avoid Windows/WSL networking pitfalls.

- "Address already in use" for port 9999
  - Stop the other listener or pick another free port and update `exp6.py` accordingly.

- "Cannot run multiple SparkContexts"
  - Only one SparkContext is allowed per JVM. Restart your interpreter/terminal if you previously ran another Spark job.

## 💡 Tips & experiments to try

- Change the batch interval in `StreamingContext(sc, batchInterval)` to smaller or larger values and observe latency vs throughput.
- Use a file or socket stream that generates more data to see how the job behaves under load.
- Replace `pprint()` with `saveAsTextFiles()` or windowed operations for more complex aggregations.
- Use structured streaming (modern API) for production workloads — it's more robust and easier to integrate with sinks.

## 🧾 Notes

- This example uses the legacy DStream API (Spark Streaming). For new projects prefer Structured Streaming (`spark.readStream` / `DataStreamReader`).
- Streaming jobs run continuously; stop with `Ctrl+C` in the Spark terminal and stop netcat with `Ctrl+C` in the data terminal.

---

If you'd like I can:
- Modify `exp6.py` to accept a `--port` CLI argument and print nicer timestamps.
- Convert this example to Structured Streaming and add a README for that.
Which would you like next?