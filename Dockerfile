FROM apache/spark:3.5.0
USER root
WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt
RUN pip install --no-cache-dir psycopg2-binary sqlalchemy pandas

# Spark Kafka connector JAR
RUN curl -L -o /opt/spark/jars/spark-sql-kafka-0-10_2.12-3.5.0.jar \
    https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.0/spark-sql-kafka-0-10_2.12-3.5.0.jar && \
    curl -L -o /opt/spark/jars/spark-token-provider-kafka-0-10_2.12-3.5.0.jar \
    https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.5.0/spark-token-provider-kafka-0-10_2.12-3.5.0.jar && \
    curl -L -o /opt/spark/jars/kafka-clients-3.4.0.jar \
    https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.4.0/kafka-clients-3.4.0.jar && \
    curl -L -o /opt/spark/jars/commons-pool2-2.11.1.jar \
    https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.11.1/commons-pool2-2.11.1.jar

# Ivy cache folder + permission
RUN mkdir -p /home/spark/.ivy2 && \
    chown -R spark:spark /home/spark
    
COPY src/ /app/src/
COPY batch/ /app/batch/
COPY spark/ /app/spark/
COPY sql/ /app/sql/
COPY streaming/ /app/streaming/

RUN mkdir -p /app/logs /app/data && \
    chown -R spark:spark /app && \
    chmod -R 777 /app

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

USER spark