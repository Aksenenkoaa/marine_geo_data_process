# marine_geo_data_process
Process of geo data from ships

python3 -m poetry install
docker network create "kafka-network"

docker-compose up
# if consumer give error "kafka.errors.NoBrokersAvailable: NoBrokersAvailable"
# check that KafkaProducer and KafkaConsumer have same api_version
# in all files with KafkaProducer and KafkaConsumer - there should be same api_version
# go into container
docker container exec -it kafka1 bash
/bin/kafka-topics --version
# result example
7.6.0-ccs
# write this in KafkaProducer and KafkaConsumer
consumer = KafkaConsumer(
'my_topic_name',
api_version=(7, 6, 0),
bootstrap_servers=['kafka1:29092'],
...)


# if run consumer locally then KAFKA_LISTENERS should be removed/commented
# if change data in docker-compose.yaml then better reload terminals
# KafkaConsumer bootstrap_servers=['localhost:29092', 'kafka1:9092',],  # for run locally


# operations with topics


# If there is error with CMD "python3 src/flink_consumer.py"
# ModuleNotFoundError: No module named '_lzma'
pyenv uninstall 3.10.13 # desired-python-version
brew install xz
pyenv install 3.10.13 # desired-python-version


