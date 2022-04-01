"""_summary_
spark-submit streaming.py
"""
from pyspark.sql import SparkSession
from pyspark.sql.avro.functions import from_avro
from pyspark.sql.functions import col

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("Multi Query Demo") \
        .master("local[3]") \
        .config("spark.streaming.stopGracefullyOnShutdown", "true") \
        .getOrCreate()

    kafka_source_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "avro_topic") \
        .option("startingOffsets", "earliest") \
        .load()

    avroSchema = open('schema/person.avsc', mode='r').read()

    value_df = kafka_source_df.select((from_avro(col("value"), avroSchema)).alias("value"))

    # value_df.show()

    write_query = value_df.writeStream \
        .format("console") \
        .option("checkpointLocation", "../chk-point-dir") \
        .outputMode("append") \
        .start()

    # Stream Processing application will only terminate when you Manual Stop or Kill or Exception & shut down gracefully
    write_query.awaitTermination()

