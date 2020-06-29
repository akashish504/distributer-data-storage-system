from kafka import KafkaConsumer

consumer = KafkaConsumer('test',bootstrap_servers=['host.docker.internal:9092'],auto_offset_reset='latest')
for message in consumer:
    print(message.value,flush=True)
