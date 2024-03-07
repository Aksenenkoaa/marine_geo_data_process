import json

import kafka


class AlertToShip():
    def __init__(self):
        self.BOOTSTRAP_SERVERS = ['kafka1:9092', 'localhost:29092']
        self.TOPIC_NAME = 'alert_info'
        self.API_VERSION = (7, 6, 0)
        self.producer = None

    def producer_start(self):
        self.producer = kafka.KafkaProducer(bootstrap_servers=self.BOOTSTRAP_SERVERS, api_version=self.API_VERSION,)

    def send_message(self, alert_data):
        print('alert_data', alert_data)
        self.producer.send(self.TOPIC_NAME, json.dumps(alert_data).encode('utf-8', 'replace'))
