from pyspark import SparkContext
from pyspark.streaming import StreamingContext

if __name__ == "__main__":
    hostname = "localhost"
    port_number = 8888

    sc = SparkContext(appName="ErrorCounter")
    ssc = StreamingContext(sparkContext=sc, batchDuration=2)

    ssc.checkpoint("/home/wesley/Documents/spark/checkpoints")

    lines = ssc.socketTextStream(hostname=hostname, port=port_number)

    error_count = lines.flatMap(lambda line: line.split(" ")) \
        .filter(lambda word: "ERROR" in word) \
        .map(lambda word: (word, 1)) \
        .reduceByKeyAndWindow(func=lambda sum_occurrences, next_occurrence: sum_occurrences + next_occurrence,
                              invFunc=lambda sum_occurrences, next_occurrence: sum_occurrences - next_occurrence,
                              windowDuration=10, slideDuration=2)

    error_count.pprint()

    ssc.start()
    ssc.awaitTermination()
