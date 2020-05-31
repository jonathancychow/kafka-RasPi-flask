
from kafka import KafkaConsumer
import sys

def start_consumer():
    # Construct kafka consumer object
    consumer = KafkaConsumer(topic, bootstrap_servers=[kafkaserver])
    for msg in consumer:
        # pring out value in msg, could have printed out the whole message as well
        print (msg.value)

if __name__ == '__main__':

    kafkaserver = sys.argv[1]   # Kafka server IP Address and Port ie 192.168.1.52:9092
    topic = sys.argv[2]         # Kafka topic ie kafka_test

    start_consumer()


