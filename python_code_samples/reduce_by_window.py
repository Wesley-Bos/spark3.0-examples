from pyspark import SparkContext
from pyspark.streaming import StreamingContext

if __name__ == "__main__":
    hostname = "localhost"
    port_number = 8888

    sc = SparkContext(appName="windowCounterUsingReduce")
    ssc = StreamingContext(sparkContext=sc, batchDuration=2)

    ssc.checkpoint("/home/wesley/Documents/spark/checkpoints")

    ''' Lines is a DStream of RDDs, it's NOT a static collection of RDDs as it's constantly being updated'''
    lines = ssc.socketTextStream(hostname=hostname, port=port_number)

    window_count = lines.reduceByWindow(
        reduceFunc=lambda sum_occurrences, next_occurrence: int(sum_occurrences) + int(next_occurrence),
        invReduceFunc=lambda sum_occurrences, next_occurrence: int(sum_occurrences) - int(next_occurrence),
        windowDuration=10, slideDuration=2)

    window_count.pprint()

    ssc.start()
    ssc.awaitTermination()
