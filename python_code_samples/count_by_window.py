from pyspark import SparkContext
from pyspark.streaming import StreamingContext

if __name__ == "__main__":
    hostname = "localhost"
    port_number = 8888

    sc = SparkContext(appName="windowCounter")
    ssc = StreamingContext(sparkContext=sc, batchDuration=2)

    ssc.checkpoint("/home/wesley/Documents/spark/checkpoints")

    ''' Lines is a DStream of RDDs, it's NOT a static collection of RDDs as it's constantly being updated'''
    lines = ssc.socketTextStream(hostname=hostname, port=port_number)

    window_count = lines.countByWindow(windowDuration=10, slideDuration=2)
    '''windowDucration = the time interval over which we want to summarize data
    slideDuration = each time the window slides over, one RDD will leave and one RDD will enter the window
    this is one RDD because the batchDuration equals the slideDuration'''

    window_count.pprint()

    ssc.start()
    ssc.awaitTermination()
