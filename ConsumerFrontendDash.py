# Inspired by https://dash.plotly.com/live-updates
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
from urllib.request import urlopen
import json
import plotly.graph_objects as go
from kafka import KafkaConsumer
import sys

def random_num():
    import random
    x =random.uniform(0,100)
    y =random.uniform(0,100)
    z =random.uniform(0,100)
    return x,y,z

def get_kafka_client():
    # return KafkaClient(hosts='192.168.2.52:9092')
    kafkaserver = sys.argv[2]
    topic = sys.argv[3]
    return KafkaConsumer(topic, bootstrap_servers=[kafkaserver])

accel = []
timestamp = []

def GetjsonData():
    json_ipaddress = "http://192.168.2.241:8085/sensors.json"
    json_data = urlopen(json_ipaddress)
    data = json.loads(json_data.read())

    global accel
    global timestamp

    for i in range((len(data['accel']['data']) - 30), len(data['accel']['data'])):
        accel.append(data['accel']['data'][i][1][1])
        timestamp.append(data['accel']['data'][i][0] / 1000)
    time = [datetime.datetime.fromtimestamp(ts) for ts in timestamp]
    return accel, time

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H3('Live Streaming Test'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ])
)

@app.callback(Output('live-update-text', 'children'), [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    x, y, z = random_num()
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('x: {0:.2f}'.format(x), style=style),
        html.Span('y: {0:.2f}'.format(y), style=style),
        html.Span('z: {0:0.2f}'.format(z), style=style)
    ]

# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'), [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    data = {
        'time': [],
        'x': []
    }

    accel, time = GetjsonData()
    data['time'] = time
    data['x'] = accel

    client = get_kafka_client()
    for msg in client:
        print (msg.value)

    # Create the graph with subplots
    # fig = plotly.tools.make_subplots(rows=1, cols=1, vertical_spacing=0.2)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['time'], y=data['x'],
                             mode='lines+markers',
                             name='lines+markers'))

    # fig['layout']['margin'] = {
    #     'l': 30, 'r': 10, 'b': 30, 't': 10
    # }
    # fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    # fig.append_trace({
    #     'x': data['time'],
    #     'y': data['x'],
    #     'name': 'Altitude',
    #     'mode': 'lines+markers',
    #     'type': 'scatter'
    # }, 1, 1)

    return fig


if __name__ == '__main__':
    # argv[1] = host port
    # argv[2] = Kafka server IP Address and Port
    # argv[3] = topic

    hostport = 8050
    app.run_server(debug=True, port=hostport)