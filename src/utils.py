import os


def create_bootstrap_servers():
    docker_key = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)
    if docker_key:
        return ['kafka1:9092']  # for docker image build
    return ['kafka1:9092', 'localhost:29092', ]  # for run locally


def create_api_version():
    return (7, 6, 0)
