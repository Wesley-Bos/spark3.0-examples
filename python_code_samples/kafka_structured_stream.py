from pyspark.sql.session import SparkSession
from pyspark.sql.functions import explode, split, col, from_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("wordCounter").getOrCreate()

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "pxl_data") \
        .option("startingOffsets", "earliest") \
        .load()

    df.printSchema()

    personStringDF = df.selectExpr("CAST(value AS STRING)")
    schema = StructType([
        StructField("id", StringType()),
        StructField("number", StringType())
        ])
    personStringDF.printSchema()

    df_json = personStringDF.withColumn("jsonData", from_json(col("value"), schema)).select("jsondata.*")
    df_json.printSchema()
    # output to terminal
    #df_json.writeStream.format("console").outputMode("append").start().awaitTermination()

    #output kafka topic
    df_json.selectExpr("id AS key", "to_json(struct(*)) AS value")\
            .writeStream\
            .format("kafka")\
            .outputMode("append")\
            .option("kafka.bootstrap.servers", "localhost:9092")\
            .option("topic", "pxl_json")\
            .option("checkpointLocation", "checkpoints")\
            .start()\
            .awaitTermination()

