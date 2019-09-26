import os


API_VERSION = '0.2'
APP_ID = os.getenv('APP_ID')
PROCESS_POOL = 5
DATABASES = {
    'PG': {
        'ENGINE': 'psycopg2',
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': '5432',
        'DATABASE': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD')
    }
}
URLS = {
    'city_id': 'http://api.openweathermap.org/data/2.5/find',
    'forecast_day':  'http://api.openweathermap.org/data/2.5/weather',
    'forecast_week': 'http://api.openweathermap.org/data/2.5/forecast'
}
OAUTH2 = {
    'SECRET_KEY': os.getenv('SECRET_KEY'),
    'CLIENT_ID': os.getenv('CLIENT_ID'),
    'BASE_URL': os.getenv('BASE_URL'),
    'TOKEN_URL': os.getenv('TOKEN_URL'),
    'AUTHORIZATION_URL': os.getenv('AUTHORIZATION_URL'),
}
