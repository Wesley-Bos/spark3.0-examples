from pyspark import SparkContext
from pyspark.streaming import StreamingContext


def word_count(new_values, last_sum):
    if last_sum is None:
        last_sum = 0
    return sum(new_values, last_sum)


if __name__ == "__main__":
    hostname = "localhost"
    port_number = 8888

    sc = SparkContext(appName="wordCount")
    ssc = StreamingContext(sparkContext=sc, batchDuration=2)

    ssc.checkpoint("/home/wesley/Documents/spark/checkpoints")

    lines = ssc.socketTextStream(hostname=hostname, port=port_number)

    words = lines.flatMap(lambda line: line.split(" ")) \
        .map(lambda word: (word, 1)) \
        .updateStateByKey(word_count)
    # if you use reduceByKey() the count will only be for the batch duration
    # if you use updateStateByKey() the count will be globally

    words.pprint()

    ssc.start()
    ssc.awaitTermination()
