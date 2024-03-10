import json

from kafka import KafkaConsumer
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, Engine
from sqlalchemy import text

from producer_alert import AlertToShip
from utils import create_bootstrap_servers, create_api_version, create_logger

FRUD_CONST_1 = 0.514444
FRUD_CONST_2 = 9.8
FRUD_MOMENTUM_THRESHOLD = 0.2
FRUD_AVG_2MIN_THRESHOLD = 0.084
RADIUS_CONST = (180.0 / 3.14) * 60 * FRUD_CONST_1
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASS = 'postgres'
DB_HOST = 'db'
DB_PORT = '5432'


def create_postgresql_table() -> Engine:
    """
    Create table in postgres

    :return: sqlalchemy Engine
    """
    db_string = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    engine = create_engine(db_string)
    with engine.connect() as conn:
        conn.execute(text("drop table if exists ship_alerts"))
        conn.commit()
        conn.execute(text("create table if not exists ship_alerts (ship_id varchar(50) unique, alerts_count int)"))
        conn.commit()

    return engine


def update_alert_count_in_db(engine_db: Engine, ship_id) -> None:
    """
    Create new row in the postgres table or update (increment + 1) if row with id exists

    :param engine_db: sqlalchemy Engine
    :param ship_id: unique id for each ship
    :return: None
    """
    with engine_db.connect() as conn:
        conn.execute(text(
            f"insert into ship_alerts (ship_id, alerts_count) \
            values('{ship_id}', 1) \
            on conflict (ship_id) \
            do \
            update set alerts_count = ship_alerts.alerts_count + 1 where ship_alerts.ship_id = '{ship_id}'"
        ))
        conn.commit()
        result = conn.execute(text("select * from ship_alerts"))
        conn.commit()
        df = pd.DataFrame(result)
        logger.info(f'result:\n{df}')


def pandas_process(consumer: KafkaConsumer, engine_db: Engine) -> None:
    """
    Processing data with pandas

    :param consumer: KafkaConsumer data. Batch of messages
    :param engine_db: sqlalchemy Engine
    :return: None
    """
    alert_producer = AlertToShip()
    alert_producer.producer_start()
    df = pd.DataFrame()
    alert_passed = False
    for message in consumer:
        payload = message.value.decode("utf-8")
        data = json.loads(payload)

        df_row = pd.DataFrame(data, index=[0])
        df = pd.concat([df, df_row])

        df['time'] = pd.to_datetime(df['time'])
        last_time = df["time"].iloc[-1]
        last_time_minus_2min = df["time"].iloc[-1] + pd.Timedelta(minutes=-2)
        df = df[(df['time'] >= last_time_minus_2min) & (df['time'] <= last_time)]

        try:
            for column_ in ['stw', 'length', 'rot']:
                df[df[column_] == ""] = np.NaN
                df[column_] = df[column_].ffill()
                df[column_] = df[column_].bfill()
                df[column_] = df[column_].astype(float)
        except ValueError as e:
            logger.error(f'There is missing data: {e}')
            continue

        df['frud_momentum_num'] = FRUD_CONST_1 * df['stw'] / ((FRUD_CONST_2 * df['length']) ** 0.5)
        df['frud_avg_2min_num'] = df['frud_momentum_num'].mean()

        df = df.tail(1)

        df['abs'] = df['rot'].abs()
        df['radius_circulation'] = RADIUS_CONST * df['stw'] / df['rot'].abs()
        df['length_3times'] = df['length'] * 3

        df['alert'] = False
        df.loc[
            (
                    (
                            (df['frud_momentum_num'] > FRUD_MOMENTUM_THRESHOLD) |
                            (df['frud_avg_2min_num'] > FRUD_AVG_2MIN_THRESHOLD)
                    ) & (df['radius_circulation'] < df['length_3times'])
            ), 'alert'] = True

        if df.iloc[0]['alert']:
            if not alert_passed:
                df['time'] = df['time'].astype(str)
                dict_last_row = df.to_dict('records')[0]

                alert_producer.send_message(alert_data=dict_last_row)
                update_alert_count_in_db(engine_db=engine_db, ship_id=dict_last_row.get('dms_id'))
                alert_passed = True
        else:
            alert_passed = False


def consumer_start(engine_db: Engine) -> None:
    """
    Create KafkaConsumer

    :param engine_db: sqlalchemy Engine
    :return: None
    """
    consumer = KafkaConsumer(
        'ship_info',
        api_version=create_api_version(),
        bootstrap_servers=create_bootstrap_servers(),
        group_id='marine_group',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        request_timeout_ms=10001,
        max_poll_interval_ms=10000,
    )
    pandas_process(consumer=consumer, engine_db=engine_db)


if __name__ == '__main__':
    logger = create_logger()
    engine_db = create_postgresql_table()
    consumer_start(engine_db=engine_db)
