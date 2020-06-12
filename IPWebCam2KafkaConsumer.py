
from kafka import KafkaConsumer
import sys
import json

def start_consumer():
    # Construct kafka consumer object
    consumer = KafkaConsumer(topic, bootstrap_servers=[kafkaserver])
    for msg in consumer:
        # pring out value in msg, could have printed out the whole message as well
        rawdata = msg.value
        stringdata = rawdata.decode()
        listdata = json.loads((stringdata))
        timestamp = listdata[0]
        gVert = listdata[1][1]
        print (timestamp)
        print (gVert)

if __name__ == '__main__':

    kafkaserver = sys.argv[1]   # Kafka server IP Address and Port ie 192.168.1.52:9092
    topic = sys.argv[2]         # Kafka topic ie kafka_test

    start_consumer()


