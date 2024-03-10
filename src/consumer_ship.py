import json

from kafka import KafkaConsumer

from utils import create_bootstrap_servers, create_api_version, create_logger


def consumer_start() -> None:
    """
    Create KafkaConsumer for getting alerts on the ship board

    :return: None
    """
    consumer = KafkaConsumer(
        'alert_info',
        api_version=create_api_version(),
        bootstrap_servers=create_bootstrap_servers(),
        group_id='marine_group',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        request_timeout_ms=10001,
        max_poll_interval_ms=10000,
    )

    for message in consumer:
        payload = message.value.decode("utf-8")
        data = json.loads(payload)
        logger.info(f'ALERT!\n{data}')


if __name__ == '__main__':
    logger = create_logger()
    consumer_start()
