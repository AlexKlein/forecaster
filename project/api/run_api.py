"""
Micro-framework launcher for the app working with routing URLs.

"""
import os
from datetime import datetime

from flask import Flask, request, redirect, session
from flask_dance.consumer import OAuth2ConsumerBlueprint
from werkzeug.middleware.proxy_fix import ProxyFix

import settings as config
from scripts.get_this_day_forecast import start_up as daily_forecast

from utils.check_permissions import get_permission
from utils.launch_tasks import start_task


API_VERSION = config.API_VERSION
CURRENT_DATE = datetime.strftime(datetime.now(), '%Y%m%d')

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)
app.secret_key = config.OAUTH2['SECRET_KEY']

oauth_blueprint = OAuth2ConsumerBlueprint(
    "oauth", __name__,
    client_id=config.OAUTH2['CLIENT_ID'],
    client_secret=config.OAUTH2['SECRET_KEY'],
    base_url=config.OAUTH2['BASE_URL'],
    token_url=config.OAUTH2['TOKEN_URL'],
    authorization_url=config.OAUTH2['AUTHORIZATION_URL'],
    redirect_url='/',
    scope='default'
)

app.register_blueprint(oauth_blueprint)


def get_user() -> dict:
    auth = session.get('oauth_oauth_token')

    if auth:
        return auth.get('user')
    return None


def check_user() -> tuple:
    user = get_user()

    if not user:
        return False, 'not_logged_in'
    else:
        user_name = user.get('username')

        if get_permission(user_name):
            return True, user_name
        else:
            return False, user_name


def format_error_json(user_name) -> dict:
    return {
        'meta':
            {
                'api_version': API_VERSION,
                'code': 403,
                'user': user_name,
                'error': 'Access denied',
                'issue_date': CURRENT_DATE,
            }
    }


@app.route("/login")
def login():
    referrer = request.headers.get("Referer")

    if referrer:
        session["next_url"] = referrer

    return redirect('oauth', 302)


@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')


@app.route('/', methods=['GET'])
def get_main():
    permission, user_name = check_user()

    if permission:
        return {
            'meta':
                {
                    'api_version': API_VERSION,
                    'code': 200,
                    'issue_date': CURRENT_DATE
                }
        }
    elif user_name == 'not_logged_in':
        referrer = request.headers.get("Referer")

        if referrer:
            session["next_url"] = referrer

        return redirect('login', 302)
    else:
        return format_error_json(user_name)


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
    permission, user_name = check_user()

    if permission:
        return daily_forecast(country, city)
    elif user_name == 'not_logged_in':
        referrer = request.headers.get("Referer")

        if referrer:
            session["next_url"] = referrer

        return redirect('login', 302)
    else:
        return format_error_json(user_name)


@app.route('/weekly/<country>,<city>', methods=['GET'])
def weekly(country, city):

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
    permission, user_name = check_user()

    if permission:
        params = {
            'method': 'start_weekly_fc',
            'param': {'country': country, 'city': city},
            'user_name': user_name
        }
        return start_task(**params)
    elif user_name == 'not_logged_in':
        referrer = request.headers.get("Referer")

        if referrer:
            session["next_url"] = referrer

        return redirect('login', 302)
    else:
        return format_error_json(user_name)


def start_up(host, port):
    app.run(host=host, port=port, debug=False)
