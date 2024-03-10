import logging
import os
import sys


def create_bootstrap_servers():
    docker_key = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)
    if docker_key:
        return ['kafka1:9092']  # for docker image build
    return ['kafka1:9092', 'localhost:29092', ]  # for run locally


def create_api_version():
    return (7, 6, 0)


def create_logger() -> logging.Logger:
    """
    This function for logger creating

    """
    logger = logging.getLogger('ship_alert')
    logger.handlers.clear()
    logger.setLevel(logging.INFO)
    handler_file = logging.FileHandler('../ship_alert.log')
    handler_stream = logging.StreamHandler(sys.stdout)
    formatter = logging \
        .Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    handler_file.setFormatter(formatter)
    handler_stream.setFormatter(formatter)
    logger.addHandler(handler_file)
    logger.addHandler(handler_stream)

    return logger
