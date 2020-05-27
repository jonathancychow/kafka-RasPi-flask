
from urllib.request import urlopen
import json
from datetime import datetime
from datetime import timedelta
# import matplotlib.animation as animation
# from matplotlib import style
from kafka import KafkaConsumer
from json import dumps
import time
import sys

def start_consumer():
    # topic = "test_1_12052020"
    consumer = KafkaConsumer(topic, bootstrap_servers=[kafkaserver])

    for msg in consumer:
        print (msg.value)

if __name__ == '__main__':
    # argv[1] = host IP Adddress
    # argv[2] = Kafka server IP Address and Port
    # argv[3] = topic
    # argv[4] = Phone IP Address

    kafkaserver = sys.argv[1]
    topic = sys.argv[2]

    start_consumer()


