## marine_geo_data_process
Обработка геоданных с морских судов
___

# Логика работы приложения:

Контейнер producer_ship (producer_ship.py) забирает данные из csv файла
и отправляет в KafkaProducer в топик ship_info.
Тем самым данный контейнер эмулирует отправку сообщений с борта корабля.

Контейнер consumer_alert приримает сообщения с борта корабля через KafkaConsumer.
В этом же контейнере производится:
+ анализ данных
+ отправка алерта на борт судна
+ сохранение счетчика алертов для каждого судна в базе данных

Анализ данных производится с помощью Pandas.
Необходимо данный функционал переписать на (по приоритетности):
+ Flink
+ Spark Structured Streaming

Отправка алертов производится с помощью модуля producer_alert.py.
В данном модуле используется KafkaProducer и топик alert_info.

Сохранение счетчиков алертов производится в Postgresql (Контейнер db).
Визуализация счетчиков алертов осуществялется 
с помощью Grafana (Контейнер grafana).

Прием алертов на борту корабля осуществляется 
с помощью контейнера consumer_ship через KafkaConsumer.

Весь код с KafkaProducer и KafkaConsumer 
реализован в пакете marine_geo_data_process/src

В директории marine_geo_data_process/y_images_for_readme
находятся изображения, используемые в качестве инструкции 
по созданию дашборда в Grafana.
___

## Подготовьте приложение:
Перенесите приложение на свою машину:

`git clone https://github.com/Aksenenkoaa/marine_geo_data_process`

Скопируйте файл "vessels_data.csv" в корневой каталог проекта (marine_geo_data_process)

Если есть какие-то проблемы в запуске docker контейнеров, 
удалите все контейнеры перед перезапуском:

`docker stop $(docker ps -aq) && docker rm $(docker ps -aq) && docker ps -a`

`docker rmi $(docker images | egrep 'producer_ship|consumer_ship|consumer_alert')`

Проверить images:
`docker images`
___

## Запустите приложение:
`docker-compose up`

Если KafkaConsumer выдает error "kafka.errors.NoBrokersAvailable: NoBrokersAvailable"
проверьте, что у KafkaProducer и KafkaConsumer 
в данном приложении указан одинаковый api_version.
Во всех файлах KafkaProducer и KafkaConsumer - должен быть одинаковый api_version. 
Чтобы узнать какой у вас api_version, зайдите в container

`docker container exec -it kafka1 bash`

`/bin/kafka-topics --version`

Вы получите api_version, например: 7.6.0-ccs
Запишите числовое значение (7.6.0) в KafkaProducer и KafkaConsumer
У вас получится примерно так:
```python
consumer = KafkaConsumer(
'my_topic_name',
api_version=(7, 6, 0),
bootstrap_servers='kafka1:9092',
...)
```
___

Если появится ошибка ModuleNotFoundError: No module named '_lzma'
то сделайте следующее:

`pyenv uninstall 3.10.0 # desired-python-version`

`brew install xz`

`pyenv install 3.10.0 # desired-python-version`
___

Вы можете регулировать скорость подачи данных с кораблей.
Если вы хотите запустить подачу данных в соотвествии с 
временной меткой 'time', которая показывает в какое время 
данные были отправлены с корабля, то установите REAL_TIME_FREQUENCY = True
Вы можете регулировать скорость подачи данных увеличивая (ускоряя)
или уменьшая (снижая скорость) значение переменной SPEED_UP
___

## Создайте dashboard:
После запуска "docker compose up", как только контейнер Grafana
запустится, перейдите по адресу http://localhost:3000

Войдите: login: admin; password: admin

Создайте источник данных (база постгрес, которую поднимаем в докере)

![create-source](https://github.com/Aksenenkoaa/marine_geo_data_process/blob/main/y_images_for_readme/create_data_source.png)

Создайте дашборд: bar chart лучше выбрать горизонтальный, так как id кораблей очень длинный 
и при вертикальном варианте id разных кораблей будут перекрывать друг друга.

![create-dash](https://github.com/Aksenenkoaa/marine_geo_data_process/blob/main/y_images_for_readme/create_dashboard.png)

Укажите с какой частотой обновлять данные в дашборде

<img src="https://github.com/Aksenenkoaa/marine_geo_data_process/blob/main/y_images_for_readme/refresh_dashboard.png" width="400">

В результате получится примерно такой дашборд

![result](https://github.com/Aksenenkoaa/marine_geo_data_process/blob/main/y_images_for_readme/result.png)
