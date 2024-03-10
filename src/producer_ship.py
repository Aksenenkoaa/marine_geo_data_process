import csv
from datetime import datetime
import json
import time

from kafka import KafkaProducer

from utils import create_bootstrap_servers, create_api_version, create_logger

REAL_TIME_FREQUENCY = True
# REAL_TIME_FREQUENCY = False
SPEED_UP = 1_000
LINGER_MS = 60_000 / SPEED_UP
BATCH_SIZE = 7_000
COMPRESSION_TYPE = 'lz4'
FORMAT = '%Y-%m-%d %H:%M:%S%z'
TOPIC_NAME = 'ship_info'
DATA_SOURCE = 'vessels_data.csv'


def producer_start() -> KafkaProducer:
    """
    Create KafkaProducer for sending messages with navy data
    from ship to the program outside the ship's board

    :return: None
    """
    return KafkaProducer(bootstrap_servers=create_bootstrap_servers(),
                         api_version=create_api_version(),
                         linger_ms=LINGER_MS,
                         batch_size=BATCH_SIZE,)
    # compression_type=COMPRESSION_TYPE,)


def send_message(producer: KafkaProducer) -> None:
    """
    Send messages from the ship to the program outside the ship's board

    :param producer: KafkaProducer
    :return: None
    """
    with open(DATA_SOURCE, 'r') as f:
        data = csv.DictReader(f)
        if REAL_TIME_FREQUENCY:
            cur_time = prev_time = None
            time_delta = 0
        for row in data:
            cur_time = datetime.strptime(row.get('time'), FORMAT)
            if REAL_TIME_FREQUENCY:
                if prev_time is not None:
                    time_delta = (cur_time - prev_time).total_seconds()

                time.sleep(time_delta / SPEED_UP)
            producer.send(TOPIC_NAME, json.dumps(row).encode('utf-8', 'replace'))

            logger.info(f'successfully sent from the ship: {row}')
            if REAL_TIME_FREQUENCY:
                prev_time = cur_time


if __name__ == '__main__':
    logger = create_logger()
    producer = producer_start()
    send_message(producer=producer)
