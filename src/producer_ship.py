import csv
from datetime import datetime
import json
import time

import kafka

from utils import create_bootstrap_servers, create_api_version

SPEED_UP = 20
LINGER_MS = 60_000 / SPEED_UP
BATCH_SIZE = 7_000
COMPRESSION_TYPE = 'lz4'
FORMAT = '%Y-%m-%d %H:%M:%S%z'
TOPIC_NAME = 'ship_info'
DATA_SOURCE = 'vessels_data.csv'
# DATA_SOURCE = 'vessels_data_test.csv'
# DATA_SOURCE = 'vessels_data_short_30_sec.csv'


def producer_start():
    producer = kafka.KafkaProducer(bootstrap_servers=create_bootstrap_servers(),
                                   api_version=create_api_version(),
                                   linger_ms=LINGER_MS,
                                   batch_size=BATCH_SIZE,)
                                   # compression_type=COMPRESSION_TYPE,)

    with open(DATA_SOURCE, 'r') as f:
        data = csv.DictReader(f)
        cur_time = prev_time = None
        time_delta = 0
        for row in data:
            cur_time = datetime.strptime(row.get('time'), FORMAT)
            # if prev_time is not None:
            #     time_delta = (cur_time - prev_time).total_seconds()
            #
            # time.sleep(time_delta / SPEED_UP)
            producer.send(TOPIC_NAME, json.dumps(row).encode('utf-8', 'replace'))

            print('successfully sent from the ship: ', row)
            prev_time = cur_time


if __name__ == '__main__':
    producer_start()