- [Kafka Data Source Spark Streaming Avro Files](#kafka-data-source-spark-streaming-avro-files)
  - [Environment setup](#environment-setup)
  - [Running steps](#running-steps)
    - [Example 1: Publishing 1000 records](#example-1-publishing-1000-records)
    - [Example 2: Publishing 10 Million records](#example-2-publishing-10-million-records)
  - [How to visualize Parquet file data](#how-to-visualize-parquet-file-data)
  - [On Error](#on-error)
  - [How to know how many messages are on broker server](#how-to-know-how-many-messages-are-on-broker-server)
  - [In Order to purge all messages from Kafka Topic](#in-order-to-purge-all-messages-from-kafka-topic)

![spark streaming](https://i.imgur.com/aGB9b0S.jpg "spark streaming using Kafka and python") 

# Kafka Data Source Spark Streaming Avro Files

> We are using python script to produce events on Kafka broker server in Avro format. Next we are using Spark to stream the records from Kafka and read it from Avro format and print on console.

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

Note: If you want to continuously generate messages then use

`python3 stream-producer.py --count 100 --cycle 10`

This script will generate `100*10 = 1000` messages. 

### Example 1: Publishing 1000 records

![](https://i.imgur.com/EHL9GIv.png)

`python3 stream-producer.py --count 1000`

![](https://i.imgur.com/otFScqS.png)

### Example 2: Publishing 10 Million records

![](https://i.imgur.com/6DjBNB6.png "Publishing 10m records")

![](https://i.imgur.com/XGKeI7X.png "File output")

Created 20MB file each when I run every 20 seconds  

![](https://i.imgur.com/IVciW1l.png)

## How to visualize Parquet file data
In order to view the Parquet file in your visual studio code use this extension i, install it and then use to visualize the file data https://marketplace.visualstudio.com/items?itemName=dvirtz.parquet-viewer


## On Error 
The beauty of spark streaming is that it uses the check point directory to save the metadata about the offset. So incase if you crash the streaming process and restart it again. Spark will start streaming from the point it left before crash. So it is fault tolerant & comes with no data loss feature! 

## How to know how many messages are on broker server 
In order to know how many messages are on queue do below.

Navigate to Kafka folder first `cd ~/kafka2` Then run any one below script. 

 
```sh
bin/kafka-run-class.sh kafka.admin.ConsumerGroupCommand --group my-group --bootstrap-server localhost:9092 --describe
OR
bin/kafka-run-class.sh kafka.admin.ConsumerGroupCommand --bootstrap-server localhost:9092 --describe --all-groups
```

 ![](https://i.imgur.com/XSekgku.png)

 ## In Order to purge all messages from Kafka Topic 

 Temporarily update the retention time on the topic to one second:

```
bin/kafka-topics.sh --zookeeper localhost:2181 --alter --topic avro_topic --config retention.ms=1000
```

This  script is not working for me though and I see below error
```
Exception in thread "main" joptsimple.UnrecognizedOptionException: zookeeper is not a recognized option
```