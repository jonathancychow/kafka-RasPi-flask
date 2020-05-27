
from urllib.request import urlopen
import json
from datetime import datetime
from datetime import timedelta
from kafka import KafkaProducer
from json import dumps
import time
import sys

def start_producer():
    # json_url = "http://10.142.208.192:8085/sensors.json"
    # json_url_string = "http://192.168.2.241:8085/sensors.json"
    json_url_string = "http://" + phoneipaddress + ":8085/sensors.json"

    time_now = datetime.now() + timedelta(seconds=-100)
    time_end = time_now + timedelta(seconds=+300)


    producer = KafkaProducer(bootstrap_servers=[kafkaserver],
                             value_serializer=lambda x: dumps(x).encode('utf-8'))


    for i in range(100):
        json_url = urlopen(json_url_string)
        data = json.loads(json_url.read())

        for j in range(20):
            data2kfaka = data['accel']['data'][i][1][1]
            Data2KfakaFormat = {'gVert' : data2kfaka}
            print(Data2KfakaFormat)
            producer.send(topic, value=Data2KfakaFormat)




if __name__ == '__main__':
    
    # argv[1] = host IP Adddress
    # argv[2] = Kafka server IP Address and Port 
    # argv[3] = topic
    # argv[4] = Phone IP Address
    hostip          = sys.argv[1]
    kafkaserver     = sys.argv[2]
    topic           = sys.argv[3]
    phoneipaddress  = sys.argv[4]

    start_producer()

  

