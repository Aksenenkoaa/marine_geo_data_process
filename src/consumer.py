import kafka

consumer = kafka.KafkaConsumer('ship_info')
for msg in consumer:
    print(msg)