from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from elasticsearch import Elasticsearch


# Create spark session :
spark = SparkSession.builder \
    .appName("Movies_consumer") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.4,"\
    "org.elasticsearch:elasticsearch-spark-30_2.12:8.11.0") \
    .getOrCreate()


# Define the schema of movies data :
schema = StructType([
    StructField("adult", BooleanType()),
    StructField("backdrop_path", StringType()),
    StructField("genre_ids", ArrayType(IntegerType())),
    StructField("original_language", StringType()),
    StructField("original_title", StringType()),
    StructField("overview", StringType()),
    StructField("popularity", FloatType()),
    StructField("poster_path", StringType()),
    # StructField("release_date", DateType()),
    StructField("release_date", DateType()),

    # StructField("release_date", date_format("release_date", "yyyy-MM-dd"), DateType()),
    StructField("title", StringType()),
    StructField("video", BooleanType()),
    StructField("vote_average", FloatType()),
    StructField("vote_count", IntegerType()),
    StructField("genre_names", ArrayType(StringType()))
])


# Read data from Kafka :
kafka_data = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "movies") \
    .load()


# Specify the value deserializer :
kafka_data = kafka_data.selectExpr("CAST(value AS STRING)")

# Parse data to JSON :
parsed_stream_df = kafka_data \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")\
    .withColumn("release_date", date_format("release_date", "yyyy-MM-dd"))\
    .withColumn("description", concat_ws(" ", col("title"), col("overview")))

# Add colonne description :
# parsed_stream_df = parsed_stream_df.withColumn("description", concat_ws(" ", col("title"), col("overview")))

print("_"*40)
print(parsed_stream_df)
print("_"*40)

parsed_stream_df.writeStream \
    .format("org.elasticsearch.spark.sql") \
    .outputMode("append") \
    .option("es.resource", "movies") \
    .option("es.nodes", "localhost") \
    .option("es.port", "9200") \
    .option("es.nodes.wan.only", "true")\
    .option("es.index.auto.create", "true")\
    .option("checkpointLocation", "./checkpointLocation/") \
    .start().awaitTermination()

parsed_stream_df.writeStream.outputMode("append").format("console").start().awaitTermination()
