
from urllib.request import urlopen
import json
from kafka import KafkaProducer
from json import dumps
import sys

def start_producer():
    json_url_string = "http://" + phoneipaddress + ":8085/sensors.json"

    producer = KafkaProducer(bootstrap_servers=[kafkaserver],
                             value_serializer=lambda x: dumps(x).encode('utf-8'))

    for i in range(100):
        json_url = urlopen(json_url_string)
        data = json.loads(json_url.read())

        for j in range(20):
            data2kfaka = data['accel']['data'][i]
            # Data2KfakaFormat = {'gVert' : data2kfaka}
            Data2KfakaFormat = data2kfaka
            print(Data2KfakaFormat)
            producer.send(topic, value=Data2KfakaFormat)

if __name__ == '__main__':

    kafkaserver     = sys.argv[1]   # Kafka server IP Address and Port ie 192.168.1.52:9092
    topic           = sys.argv[2]   # Kafka topic ie kafka_test
    phoneipaddress  = sys.argv[3]   # IP Address of the Phone where IPWebcam is running ie 192.168.2.241

    start_producer()

  

