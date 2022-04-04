- [Kafka Data Source Spark Streaming Avro Files & Saving in Parquet Format](#kafka-data-source-spark-streaming-avro-files--saving-in-parquet-format)
  - [Environment setup](#environment-setup)
  - [Running steps](#running-steps)
    - [Example 1: Spark Streaming Kafka Messages to In-Memory Console](#example-1-spark-streaming-kafka-messages-to-in-memory-console)
    - [Example 2: Spark Streaming 10 million Kafka records to Parquet files](#example-2-spark-streaming-10-million-kafka-records-to-parquet-files)
  - [How to visualize Parquet file data](#how-to-visualize-parquet-file-data)
  - [On Error](#on-error)
  - [How to know how many messages are on broker server](#how-to-know-how-many-messages-are-on-broker-server)
  - [In Order to purge all messages from Kafka Topic](#in-order-to-purge-all-messages-from-kafka-topic)
  - [Using AWS MSK](#using-aws-msk)

![spark streaming](https://i.imgur.com/aGB9b0S.jpg 'spark streaming using Kafka and python')

# Kafka Data Source Spark Streaming Avro Files & Saving in Parquet Format

> We are using python script to produce events on Kafka broker server in Avro format. Next we are using Spark to stream the records from Kafka and read it from Avro format and print on console.

## Environment setup

Most important thing is to match the version this sample is working with below versions. Make sure you have that version only before running scripts.

- Install python, I have python `v3.9`
- Install `confluent_kafka` here is the script `pip install confluent_kafka`
  ![](https://i.imgur.com/5CfyhFw.png)
- Since I am using Avro files. You have to install `avro` package.
- Install `avro` package `pip3 install avro` So that in python code you can use `avro` package. You can use pip if u r using `bash`. If you are using `.zshrc` then use `pip3`
  ![](https://i.imgur.com/3m1y08Z.png)
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

## Running steps

1. Run zookeeper server `01-start-zookeeper.sh`
2. Run kafka server `02-start-kafka.sh`
3. Run `python3 producer.py`
4. Run `spark-submit streaming.py`

Check the job analytics at spark context UI at http://localhost:4040/jobs/

Note: If you want to continuously generate messages then use

`python3 stream-producer.py --count 100 --cycle 10`

This script will generate `100*10 = 1000` messages.

### Example 1: Spark Streaming Kafka Messages to In-Memory Console

- **publisher** script: `python3 stream-producer.py --count 1000 --cycle 1`
- **Subscriber** script: `spark-submit streming-in-memory.py`

![](https://i.imgur.com/EHL9GIv.png)

![](https://i.imgur.com/otFScqS.png)

### Example 2: Spark Streaming 10 million Kafka records to Parquet files

- **publisher** script: `python3 stream-producer.py --count 10000 --cycle 1000`
- **subscriber** script `spark-submit streaming-to-parquet-file.py`

![](https://i.imgur.com/6DjBNB6.png 'Publishing 10m records')

![](https://i.imgur.com/XGKeI7X.png 'File output')

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

This script is not working for me though and I see below error

```
Exception in thread "main" joptsimple.UnrecognizedOptionException: zookeeper is not a recognized option
```

## Using AWS MSK

If you are using AWS Managed Stream Kafka as your Kafka Broker. Then you need a EC2 instance to produce events. I have created `cloud9` environment and using event producer to produce event. You can do the same. However, make sure you are going to MSK security group and adding the inbound rule to allow all traffic from `cloud9` EC2 instance security group.

![](https://i.imgur.com/vOpyI2C.png)

I love cloud9 it is basically an EC2 instance pre installed with python,node.js, JAVA etc. Also it gives you an on-line IDE which is very similar to VSCode. I am enjoying a lot with `cloud9` try using it.
![](https://i.imgur.com/YUaq9TC.png)
