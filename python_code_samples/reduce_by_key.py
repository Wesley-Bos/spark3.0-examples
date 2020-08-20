from pyspark import SparkContext
from pyspark.streaming import StreamingContext

if __name__ == "__main__":
    hostname = "localhost"
    port_number = 8888

    sc = SparkContext(appName="ErrorCounter")
    ssc = StreamingContext(sparkContext=sc, batchDuration=2)
    ''' batchDuration=2 --> all messages received within a 2s window from one RDD within the DStream. '''

    ''' Create a new directory, this one will be used as a checkpoint storagepoint.'''
    ssc.checkpoint("/home/wesley/Documents/spark/checkpoints")

    ''' Lines is a DStream of RDDs, it's NOT a static collection of RDDs as it's constantly being updated'''
    lines = ssc.socketTextStream(hostname=hostname, port=port_number)

    error_count = lines.flatMap(lambda line: line.split(" ")) \
        .filter(lambda word: "ERROR" in word) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda sum_occurrences, next_occurrence: sum_occurrences + next_occurrence)

    '''  Print out the result.'''
    error_count.pprint()

    '''# Start listening for streaming data.'''
    ssc.start()
    '''  Wait infinitely for streaming data unless you explicitly terminate the application.'''
    ssc.awaitTermination()
