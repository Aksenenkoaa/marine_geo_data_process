import csv
from datetime import datetime
import json

import kafka

BOOTSTRAP_SERVERS = 'localhost:9092'
FORMAT = '%Y-%m-%d %H:%M:%S%z'
TOPIC_NAME = 'ship_info'
DATA_SOURCE = 'vessels_data_short.csv'


def producer_start():
    producer = kafka.KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    with open(DATA_SOURCE, 'r') as f:
        data = csv.DictReader(f)
        for row in data:
            cur_minute = datetime.strptime(row.get('time'), FORMAT).replace(second=0)
            print(cur_minute)
            producer.send(TOPIC_NAME, json.dumps(row).encode('utf-8', 'replace'))