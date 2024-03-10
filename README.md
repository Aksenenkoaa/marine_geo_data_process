### marine_geo_data_process
Process of geo data from ships


## Prepere program:
git clone https://github.com/Aksenenkoaa/marine_geo_data_process
### copy file "vessels_data.csv" to the project root (marine_geo_data_process)
docker compose up
### if there are some problem, remove all containers before restart
docker stop $(docker ps -aq) && docker rm $(docker ps -aq) && docker ps -a
docker rmi $(docker images | egrep 'producer_ship|consumer_ship|consumer_alert')
### to check images:
docker images


## To start program:
docker-compose up
### if consumer give error "kafka.errors.NoBrokersAvailable: NoBrokersAvailable"
### check that KafkaProducer and KafkaConsumer have same api_version
### in all files with KafkaProducer and KafkaConsumer - there should be same api_version
### go into container
docker container exec -it kafka1 bash
/bin/kafka-topics --version
### result example
7.6.0-ccs
### write this in KafkaProducer and KafkaConsumer
consumer = KafkaConsumer(
'my_topic_name',
api_version=(7, 6, 0),
bootstrap_servers='kafka1:9092',
...)

### If there is error with CMD "python3 src/flink_consumer.py"
### ModuleNotFoundError: No module named '_lzma'
pyenv uninstall 3.10.0 ### desired-python-version
brew install xz
pyenv install 3.10.0 ### desired-python-version

### if you need real-time frequency of sending messages from the ship board
### then you need switch REAL_TIME_FREQUENCY to True
### with SPEED_UP you could change speed of the data sending


### to construct dashboard:
### After launch "docker compose up" go to the http://localhost:3000
# login/password admin/admin

![img.png](img.png)
![img_1.png](img_1.png)
![img_2.png](img_2.png)
![img_3.png](img_3.png)
![img_4.png](img_4.png)
