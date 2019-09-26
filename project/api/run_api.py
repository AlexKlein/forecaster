"""
Micro-framework launcher for the app working with routing URLs.

"""
import os
from datetime import datetime

from flask import Flask

import settings as config
from scripts.get_this_day_forecast import start_up as daily_forecast


API_VERSION = config.API_VERSION
CURRENT_DATE = datetime.strftime(datetime.now(), '%Y%m%d')

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_main():
    return {
        'meta':
            {
                'api_version': API_VERSION,
                'code': 200,
                'issue_date': CURRENT_DATE
            }
    }


@app.route('/daily/<country>,<city>', methods=['GET'])
def daily(country, city):
    if not country or not city:
        return {
            'meta':
                {
                    'api_version': API_VERSION,
                    'code': 500,
                    'error': 'You have to set country and city',
                    'issue_date': CURRENT_DATE,
                    'country': country,
                    'city': city
                }
        }
    return daily_forecast(country, city)


def start_up(host, port):
    app.run(host=host, port=port, debug=False)
