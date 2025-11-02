
# Lab_sem5_bdtt

This repository contains two sets of example labs for distributed data processing: a `Hadoop/` folder with MapReduce Java examples and a `Spark/` folder with PySpark example scripts. Each folder contains multiple experiments with small input datasets and a short README where applicable.

## Structure

- `Hadoop/`
	- A set of Java MapReduce experiments (Exp-1 .. Exp-5).
	- Each experiment folder typically contains Java source files, small sample input files, and a README describing the individual experiment.
	- Files included (high-level):
		- `Exp-1/` — Word Count example
			- `WC_Mapper.java`, `WC_Reducer.java`, `WC_Driver.java`, `input.txt`, `Readme.md`
		- `Exp-2/` — Max Temperature example
			- `MaxTemperature.java`, `MaxTempMapper.java`, `MaxTempReducer.java`, `weather.csv`, `README.md`
		- `Exp-3/` — Students / data-processing example
			- `students.csv`, `README.md`
		- `Exp-4/` — SequenceFile example
			- `SequenceFileWriterExample.java`, `README.md`
		- `Exp-5/` — Map-side join example
			- `MapSideJoinDriver.java`, `MapSideJoinMapper.java`, `customers.txt`, `orders.txt`, `README.md`

- `Spark/`
	- PySpark example scripts (EXP-1 .. EXP-7) and a `pyproject.toml` at the root of the Spark folder.
	- Each experiment folder contains `expN.py` and usually a `README.md` and small sample data where needed.
	- Files included (high-level):
		- `EXP-1/` — `exp1.py`
		- `EXP-2/` — `exp2.py`, `sample.txt`
		- `EXP-3/` — `exp3.py`
		- `EXP-4/` — `exp4.py`
		- `EXP-5/` — `exp5.py`, `people.csv`
		- `EXP-6/` — `exp6.py`
		- `EXP-7/` — `exp7.py`

## Purpose

These labs are educational examples demonstrating common big-data patterns:

- MapReduce programming with Hadoop in Java (mappers, reducers, drivers, joins, SequenceFile usage).
- PySpark scripts demonstrating RDD/DataFrame operations and small data analysis tasks.

Each experiment is intentionally small and self-contained so you can run it locally (in standalone or pseudo-distributed mode) or on a cluster for learning.

## Requirements

- For Hadoop experiments:
	- JDK (8+), Apache Hadoop (configured locally or accessible cluster), and `javac`/`jar` available.
- For Spark experiments:
	- Python 3.x and Apache Spark (or a Spark distribution with `spark-submit`).
	- Optionally a Python virtual environment and deps managed by `pyproject.toml` in the `Spark/` folder.

## How to run (examples)

Below are minimal examples to run the experiments. Adjust class names, paths, and Hadoop/Spark configuration as appropriate for your environment.

Hadoop (from a machine with `hadoop` available):

```bash
# compile and build a jar (example for Exp-1 Word Count)
cd Hadoop/Exp-1
javac -classpath "$(hadoop classpath)" -d classes WC_*.java
jar -cvf wc.jar -C classes .

# run the MapReduce job (input and output paths are examples)
hadoop jar wc.jar WC_Driver input.txt output-wc
```

Notes:
- On Windows, run these commands in a WSL shell or in an environment where `hadoop` is available.
- Replace `WC_Driver` with the fully qualified driver class name if package statements are used.

Spark (use `spark-submit` for each `expN.py`):

```bash
# run an example Spark script locally
cd Spark/EXP-1
spark-submit --master local[*] exp1.py
```

If you prefer to run the Python file directly (without Spark cluster features), some simple scripts may run with plain Python, but `spark-submit` is the recommended way.

## Where to find more details

- Each experiment folder usually contains its own `README.md` with experiment-specific notes and sample data. Check the folder for additional details.

## Contributing / Extending

- To add an experiment, create a new `Exp-<n>/` (Hadoop) or `EXP-<n>/` (Spark) folder, include source, a small sample input and a short README explaining the objective and how to run it.

## License

This repository contains educational examples. No license file is included by default — add one if you want to set explicit reuse terms.

---

If you want, I can:

- Add a short top-level table of contents linking directly to each experiment folder.
- Add example build scripts (Makefile / build.sh) for Hadoop compilation and jar creation.
- Create a simple requirements file or `pyproject` adjustments for the `Spark/` folder.

Tell me which of those you'd like next.
