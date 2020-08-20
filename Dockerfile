# Base image to start from.
FROM ubuntu:20.04



# Information surrounding the creator.
LABEL maintainer="boswesley@live.nl"
LABEL version="0.1"
LABEL description="Docker image to setp up Apache Spark standalone."

# Update the system.
RUN apt-get update \ 
 && apt-get install -qq -y curl vim net-tools \
 && rm -rf /var/lib/apt/lists/*

# Install Python
RUN apt-get update \
 && apt-get install -y python3 \ 
 && ln -s /usr/bin/python3 /usr/bin/python \
 && rm -rf /var/lib/apt/lists/*

# Install Java
RUN apt-get update \
 && apt-get install -y openjdk-11-jre \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install Spark
RUN apt-get update -y \
 && apt-get install -y curl \
 && curl https://archive.apache.org/dist/spark/spark-3.0.0/spark-3.0.0-bin-hadoop2.7.tgz -o spark.tgz \
 && tar -xf spark.tgz \
 && mv spark-3.0.0-bin-hadoop2.7 /opt/spark/ \
 && rm spark.tgz

# Set Spark environment
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

# EXPOSE CONTAINER PORTS
EXPOSE 4040 6066 7077 8080

# SET WORKING DIR
WORKDIR $SPARK_HOME

# Copy files
COPY log4j.properties $SPARK_HOME/conf
COPY supplementary_files $SPARK_HOME/supplementary_files
COPY python_code_samples $SPARK_HOME/python_code_samples

# Run commands
CMD ["bin/spark-class", "org.apache.spark.deploy.master.Master", "org.apache.spark.deploy.worker.Worker"]
