from flask import Flask
from pymongo import MongoClient
from bson.json_util import dumps
from datetime import datetime
from kafka import KafkaConsumer
from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers=['host.docker.internal:9092'],value_serializer=lambda x:dumps(x).encode('utf-8'))

consumer = KafkaConsumer(bootstrap_servers=['host.docker.internal:9092'],auto_offset_reset='latest')


mongo = MongoClient('mongodb://mongo/test').db
# mongo = MongoClient('mongodb://localhost:27017').db


consumer.subscribe(['node_1'])
for message in consumer:
	data = json.loads(message.value.decode("utf-8"))
	if data["operation"] == "insert":
		insert_response = mongo.record_table.insert_one({
			"key": data["key"],
			"value": data["value"],
		})
		producer.send("result",str(insert_response.inserted_id))
	elif data["operation"] == "query" and 'key' in data:
		response = mongo.record_table.find_one({
			"key": data["key"]
		})
		if response:
			producer.send("result", str(response["value"]))
		else:
			producer.send("result", "Invalid Request")
	else:
		producer.send("result", "Invalid Request")
