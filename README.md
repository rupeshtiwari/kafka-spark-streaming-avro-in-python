![spark streaming](https://i.imgur.com/aGB9b0S.jpg "spark streaming using Kafka and python") 

# Kafka Data Source Spark Streaming Avro Files

> We are using python script to produce events on Kafka in Avro format. Next we are using Spark to stream the records from Kafka and read it from Avro format and print on console.

## Environment setup

Most important thing is to match the version this sample is working with below versions. Make sure you have that version only before running scripts.

- python `v3.9`
- Add below line entry in `spark-3.2.1-bin-hadoop3.2/conf/spark-defaults.conf` file.
  `spark.jars.packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,org.apache.spark:spark-avro_2.12:3.2.1`
- Add below lines on `~/.zshrc` file
  ```shell
  export JAVA_HOME=`/usr/libexec/java_home`
  export SPARK_HOME=/Users/rupeshti/spark3/spark-3.2.1-bin-hadoop3.2
  export PATH=$PATH:$SPARK_HOME/bin
  export PYSPARK_PYTHON=python3
  export KAFKA_HOME=/Users/rupeshti/kafka2
  export PATH=$PATH:$KAFKA_HOME/bin
  ```
- Install `avro` package `pip3 install avro` so that in python code you can use `avro` package.
- Install `confluent_kafka` we are using to produce events in Kafka

## Running steps

1. Run zookeeper server `01-start-zookeeper.sh`
2. Run kafka server `02-start-kafka.sh`
3. Run `python3 producer.py`
4. Run `spark-submit streaming.py`

Check the job analytics at spark context UI at http://localhost:4040/jobs/ 
