### marine_geo_data_process
### Обработка геоданных с морских судов


## Подготовьте приложение:
git clone https://github.com/Aksenenkoaa/marine_geo_data_process
### скопируйте файл "vessels_data.csv" в корневой каталог проекта (marine_geo_data_process)
### если есть какие-то проблемы в запуске docker контейнеров, 
### удалите все контейнеры перед перезапуском
docker stop $(docker ps -aq) && docker rm $(docker ps -aq) && docker ps -a
docker rmi $(docker images | egrep 'producer_ship|consumer_ship|consumer_alert')
### проверить images:
docker images


## Запустите приложение:
docker-compose up
### если KafkaConsumer дает error "kafka.errors.NoBrokersAvailable: NoBrokersAvailable"
### проверьте, что у KafkaProducer и KafkaConsumer 
### в данном приложении указан одинаковый api_version
### во всех файлах KafkaProducer и KafkaConsumer - должен быть одинаковый api_version
### чтобы узнать какой у вас api_version, зайдите в container
docker container exec -it kafka1 bash
/bin/kafka-topics --version
### вы получите api_version
7.6.0-ccs
### запишите числовое значение (7.6.0) в KafkaProducer и KafkaConsumer
### у вас получится примерно так:
consumer = KafkaConsumer(
'my_topic_name',
api_version=(7, 6, 0),
bootstrap_servers='kafka1:9092',
...)

### если появится ошибка
### ModuleNotFoundError: No module named '_lzma'
### то сделайте следующее
pyenv uninstall 3.10.0 ### desired-python-version
brew install xz
pyenv install 3.10.0 ### desired-python-version

### Вы можете регулировать скорость подачи данных с кораблей
### если вы хотите запустить подачу данных в соотвествии с 
### временной меткой 'time', которая показывает в какое время 
### данные были отправлены с корабля, то установите REAL_TIME_FREQUENCY = True
### Вы можете регулировать скорость подачи данных увеличивая (ускоряя)
### или уменьшая (снижая скорость) значение переменной SPEED_UP


### Для того чтобы сформировать dashboard:
### После запуска "docker compose up" перейдите по адресу http://localhost:3000
# login/password admin/admin

![Screenshot](img.png)
![img_1.png](img_1.png)
![img_2.png](img_2.png)
![img_3.png](img_3.png)
![img_4.png](img_4.png)
