import json

import pandas as pd
from kafka import KafkaConsumer

from producer_alert import AlertToShip
from utils import create_bootstrap_servers, create_api_version

pd.set_option('display.max_columns', None)

# API_VERSION = (7, 6, 0)
FRUD_CONST_1 = 0.514444
FRUD_CONST_2 = 9.8
FRUD_MOMENTUM_THRESHOLD = 0.2
# FRUD_AVG_2MIN_THRESHOLD = 0.84
FRUD_AVG_2MIN_THRESHOLD = 0.13
# FRUD_AVG_2MIN_THRESHOLD = 0.13
RADIUS_CONST = (180.0 / 3.14) * 60 * 0.514444


def consumer_start():

    #создание потребителя Kafka
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
    print('qqq100')

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

        df['stw'] = df['stw'].astype(float)
        df['length'] = df['length'].astype(float)
        df['rot'] = df['rot'].astype(float)

        df['frud_momentum_num'] = FRUD_CONST_1 * df['stw'] / ((FRUD_CONST_2 * df['length']) ** 0.5)
        df['frud_avg_2min_num'] = df['frud_momentum_num'].mean()

        df = df.tail(1)

        df['abs'] = df['rot'].abs()
        df['radius_circulation'] = RADIUS_CONST * df['stw'] / df['rot'].abs()
        df['length_3times'] = df['length'] * 3

        df['alert'] = False
        df.loc[df['frud_momentum_num'] > FRUD_MOMENTUM_THRESHOLD, 'alert'] = True
        df.loc[df['frud_avg_2min_num'] > FRUD_AVG_2MIN_THRESHOLD, 'alert'] = True
        df.loc[df['radius_circulation'] < df['length_3times'], 'alert'] = True

        print(df)
        if df.iloc[0]['alert']:
            if not alert_passed:
                print('zzzzz')
                df['time'] = df['time'].astype(str)
                alert_producer.send_message(df.to_dict('records')[0])
                alert_passed = True
        else:
            alert_passed = False


if __name__ == '__main__':
    consumer_start()
