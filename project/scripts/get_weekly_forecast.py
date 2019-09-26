"""
ETL process for getting thirty days weather forecast over API and load it in PostgreSQL database.

"""
import sys
from datetime import datetime

import pandas as pd
import requests

import settings as config
from api import postgres_wrapper
from utils import log_json_data


API_VERSION = config.API_VERSION
APP_ID = config.APP_ID
CURRENT_DATE = datetime.strftime(datetime.now(), '%Y-%m-%d')
URL_GET_CITY_ID = config.URLS['city_id']
URL_GET_FORECAST = config.URLS['forecast_week']


def get_city_id(country, city) -> int:
    try:
        json_data = requests.get(
            URL_GET_CITY_ID,
            params={
                'q': f"""{city},{country}""",
                'type': 'like',
                'units': 'metric',
                'APPID': APP_ID
            }
        ).json()
        extend_params = f"""'q': '{city},{country}', 
                            'type': 'like', 
                            'units': 'metric', 
                            'APPID': {APP_ID}"""
        log_json_data.log_data(json_data=json_data,
                               URL=URL_GET_CITY_ID,
                               extend=extend_params)
        return json_data["list"][0]["id"]
    except Exception as e:
        print("You've got API connection error:", e)
        sys.exit(1)


def get_weather_forecast(city_id) -> dict:
    try:
        json_data = requests.get(
            URL_GET_FORECAST,
            params={
                'id': city_id,
                'units': 'metric',
                'lang': 'en',
                'APPID': APP_ID
            }
        ).json()
        extend_params = f"""'id': '{city_id}', 
                            'APPID': {APP_ID}"""

        log_json_data.log_data(json_data=json_data,
                               URL=URL_GET_FORECAST,
                               extend=extend_params)
        return json_data
    except Exception as e:
        print("You've got API connection error", e)
        sys.exit(1)


def upload_data(data_set, conn, country, city):
    for index, row in data_set.iterrows():
        delete_query = f"""delete from fc_weekly_weather 
                                       where  value_day = date'{row['value_day']}' and 
                                              city = '{city}' and
                                              country = '{country}'"""
        insert_query = f"""insert into fc_weekly_weather (value_day,
                                                          country,
                                                          city,
                                                          temp,
                                                          pressure,
                                                          humidity,
                                                          source) values ('{row['value_day']}', 
                                                                          '{row['country']}', 
                                                                          '{row['city']}',
                                                                          '{row['temp']}', 
                                                                          '{row['pressure']}', 
                                                                          '{row['humidity']}', 
                                                                          '{row['source']}')"""
        conn.execute(raw_sql=delete_query)
        conn.execute(raw_sql=insert_query)

    conn.execute(raw_sql='commit')


def start_up(country, city):
    try:
        temp = dict()
        city_id = get_city_id(country, city)
        json_data = get_weather_forecast(city_id)
        data_set = pd.DataFrame(columns=['value_day',
                                         'country',
                                         'city',
                                         'temp',
                                         'pressure',
                                         'humidity',
                                         'source'])

        if int(json_data['cod']) == 200:

            for i in range(len(json_data['list'])):

                if str(json_data['list'][i]['dt_txt']).find('15:00:00') >= 0:
                    temp['value_day'] = datetime.strftime(
                        datetime.strptime(
                            json_data['list'][i]['dt_txt'],
                            '%Y-%m-%d %H:%M:%S'),
                        '%Y-%m-%d')
                    temp['country'] = country
                    temp['city'] = city
                    temp['temp'] = json_data['list'][i]['main']['temp']
                    temp['pressure'] = json_data['list'][i]['main']['pressure']
                    temp['humidity'] = json_data['list'][i]['main']['humidity']
                    temp['source'] = 'openweathermap'
                    data_set = data_set.append(temp, ignore_index=True)

            connection = postgres_wrapper.PostgresWrapper()
            upload_data(data_set, connection, country, city)

        return {
            'meta':
                {
                    'api_version': API_VERSION,
                    'code': 200,
                    'issue_date': CURRENT_DATE
                }
        }
    except Exception as e:
        return {
            'meta':
                {
                    'api_version': API_VERSION,
                    'code': 404,
                    'error':
                        {
                            'message': 'Results not found',
                            'type': str(e)
                        },
                    'issue_date': CURRENT_DATE
                }
        }
