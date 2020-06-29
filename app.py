from flask import Flask,request, Response
from kafka import KafkaProducer
from kafka import KafkaConsumer
from json import dumps

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x: dumps(x).encode('utf-8'))

consumer = KafkaConsumer(bootstrap_servers=['localhost:9092'], auto_offset_reset='latest',consumer_timeout_ms=1000)
consumer.subscribe(['result'])
app = Flask(__name__)


@app.route("/")
def home():
    return dumps({'Version': 1.2, 'health': 'Working Fine'})


@app.route("/insert", methods=['POST'])
def insert():
    if len(request.form['key']) <= 5:
        producer.send("node_1", {'operation': 'insert',
                                'key': request.form['key'],
                                'value': request.form['value']})
    elif 5 <= len(request.form['key']) <= 15:
        producer.send("node_2", {'operation': 'insert',
                                 'key': request.form['key'],
                                 'value': request.form['value']})
    else:
        producer.send("node_3", {'operation': 'insert',
                                 'key': request.form['key'],
                                 'value': request.form['value']})

    return Response(get_data())

@app.route("/get_items", methods=['POST'])
def get_items():
    if len(request.form['key']) <= 5:
        producer.send("node_1", {'operation': 'query',
                                 'key': request.form['key']})
    elif 5 <= len(request.form['key']) <= 15:
        producer.send("node_2", {'operation': 'query',
                                 'key': request.form['key']})
    else:
        producer.send("node_3", {'operation': 'query',
                                 'key': request.form['key']})

    return Response(get_data())


def get_data():
    for msg in consumer:
        print(msg.value)
        return msg.value


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
