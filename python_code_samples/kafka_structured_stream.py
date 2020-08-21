from pyspark.sql.session import SparkSession
from pyspark.sql.functions import explode, split, col, from_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("wordCounter").getOrCreate()
    
    # Read the data from kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "pxl_data") \
        .option("startingOffsets", "earliest") \
        .load()
    
    # Print out the dataframa schema
    #df.printSchema()
    
    # Convert the datatype for value to a string
    string_df = df.selectExpr("CAST(value AS STRING)")
    
    # Print out the new dataframa schema
    #string_df.printSchema()
    
    # Create a schema for the df
    schema = StructType([
        StructField("id", StringType()),
        StructField("number", StringType())
        ])
    
    # Select the data present in the column value and apply the schema on it
    json_df = string_df.withColumn("jsonData", from_json(col("value"), schema)).select("jsondata.*")
    
    # Print out the dataframa schema
    #json_df.printSchema()
    
    # Write output to the terminal
    #json_df.writeStream.format("console").outputMode("append").start().awaitTermination()

    # Write output to kafka topic
    json_df.selectExpr("id AS key", "to_json(struct(*)) AS value")\
            .writeStream\
            .format("kafka")\
            .outputMode("append")\
            .option("kafka.bootstrap.servers", "localhost:9092")\
            .option("topic", "pxl_json")\
            .option("checkpointLocation", "checkpoints")\
            .start()\
            .awaitTermination()

