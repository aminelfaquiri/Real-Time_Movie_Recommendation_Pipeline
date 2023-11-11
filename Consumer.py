from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# create spark session :
spark = SparkSession.builder \
    .appName("Movies_consumer") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.4") \
    .getOrCreate()


kafka_data = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "movies") \
    .load()


# Specify the value deserializer
# kafka_data = kafka_data.selectExpr("CAST(value AS STRING)")

print("_"*40)
print(kafka_data)
print("_"*40)

kafka_data.writeStream.outputMode("append").format("console").start().awaitTermination()