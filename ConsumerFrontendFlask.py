from flask import Flask, render_template, Response
from kafka import KafkaConsumer
import sys

def get_kafka_client():
    # return KafkaClient(hosts='192.168.2.52:9092')
    kafkaserver = sys.argv[2]
    topic = sys.argv[3]
    return KafkaConsumer(topic, bootstrap_servers=[kafkaserver])

app = Flask(__name__)

@app.route('/')
def index():
    return(render_template('index.html'))

# #Consumer API
@app.route('/topic/<topicname>')
def get_messages(topicname):
    client = get_kafka_client()
    def events():
        # for i in client.topics[topicname].get_simple_consumer():
        #     yield 'data:{0}\n\n'.format(i.value.decode())
        for i in client:
            yield 'data:{0}\n\n'.format(i.value)
    return Response(events(), mimetype="text/event-stream")

if __name__ == '__main__':
    
    # argv[1] = host IP Adddress
    # argv[2] = Kafka server IP Address and Port 
    # argv[3] = topic

    hostip = sys.argv[1]
    app.run(debug=True, port=5001, host=hostip)