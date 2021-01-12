# Spark_3.0-examples
View my [blog post](https://medium.com/@wesleybos99/structured-streaming-in-spark-3-0-using-kafka-db44cf871d7a?sk=5bd6d88ac86bf0f5489e97549170ebab) to get started with Apache Spark. This readme only covers the setup phases. To get a more extensive explanation, view the article.

# NOTE: Currently there is a problem with the 'psycopg2' package which I think also causes problems with a package used in the 'Spark structured streaming'. This seems to be only recently. I will look into solving this issue but know that I don't have the time to actively work on this project. (12/01/2021)
*The normal Spark shell still works so one can use that if desired.*

**Prerequisites**
* This project uses Docker and docker-compose. View [this link](https://docs.docker.com/compose/install/) to find out how to install them for your OS.

* Before we begin, create a new environment. I use Anaconda to do this but feel free to use any tool of your liking.Activate the environment and install the required libraries by executing the following commands:

        sudo apt-get install python-psycopg2
        pip install -r requirements.txt
  **Note:** depending on your pip and Python version, the commands differ a little:
  * pip becomes pip3
  * python become python3

## Spark interactive shell
1. Execute the following commands to launch Spark:

        docker build -t pxl_spark -f Dockerfile .
        docker run --rm --network host -it pxl_spark /bin/bash
2. Launch the interactive shell:

        pyspark

## Spark application - on a standalone cluster
1. Initiate the Spark container:

        docker run --rm --network host -it pxl_spark /bin/bash
2. Start a master:

        start-master.sh

    Visit the [web UI](http://localhost:8080/) and copy the URL of the Spark Master.        

3. Start a worker:

        start-slave.sh URL_MASTER
4. Launch application:

        spark-submit --master URL_MASTER examples/src/main/python/pi.py 10
       
## Spark application - streaming data
1. Open a new terminal and run the following command:

        nc -lC 8888

    Netcat will be used to send data to port 8888; simulating a stream of data.

2. Back in the Spark container, run any of the provided code examples:

       spark-submit python_code_samples/update_by_key.py

## Spark structured streaming
1. Launch the Kafka environment:

        docker-compose -f ./kafka/docker-compose.yml up -d
2. Produce and consume data:
  
    *For convenience, open two terminals beside each other.*

        python kafka/producer.py
        python kafka/consumer.py
3. Submit the application to Spark (inside Spark container):

        spark-submit --packages org.apache.spark:spark-sql-kafka-0–10_2.12:3.0.0 python_code_samples/kafka_structured_stream.py
4. Open a new terminal and start the new_consumer:

        python kafka/new_consumer.py

    In the **producer terminal**, enter data; both consumers will display this data. The messages can be seen in the  
    Confluent Control centre as well.
