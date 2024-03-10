import json

from kafka import KafkaProducer

from utils import create_bootstrap_servers, create_api_version, create_logger


class AlertToShip():
    def __init__(self):
        self.BOOTSTRAP_SERVERS = create_bootstrap_servers()
        self.TOPIC_NAME = 'alert_info'
        self.API_VERSION = create_api_version()
        self.producer = None
        self.logger = create_logger()

    def producer_start(self) -> None:
        """
        Create KafkaProducer for sending messages with alerts
        from the program outside the ship's board to the ship

        :return: None
        """
        self.producer = KafkaProducer(bootstrap_servers=self.BOOTSTRAP_SERVERS, api_version=self.API_VERSION,)

    def send_message(self, alert_data: dict) -> None:
        """
        Send messages (alerts) from the program outside the ship's board to the ship

        :param alert_data: Dict with data to send to the ship
        :return: None
        """
        self.logger.info(f'alert_data: {alert_data}')
        self.producer.send(self.TOPIC_NAME, json.dumps(alert_data).encode('utf-8', 'replace'))
