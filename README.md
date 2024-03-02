# marine_geo_data_process
Process of geo data from ships

python3 -m poetry install

docker-compose up
# go into container
docker container exec -it kafka_marine bash

# operations with topics
docker-compose exec kafka kafka-topics --bootstrap-server localhost:9092 --create --replication-factor 1 --partitions 1 --topic test_topic
docker-compose exec kafka kafka-topics --list --bootstrap-server localhost:9092
docker-compose exec kafka kafka-topics --bootstrap-server localhost:9092 --describe --topic test_topic

docker-compose exec kafka kafka-console-producer --bootstrap-server localhost:9092 --topic test_topic
docker-compose exec kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic test_topic --from-beginning

docker-compose exec kafka kafka-topics --bootstrap-server localhost:9092 --delete --topic test_topic
