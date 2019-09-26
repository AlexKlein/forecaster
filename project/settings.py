API_VERSION = '0.1'
APP_ID = ''
DATABASES = {
    'PG': {
        'ENGINE': 'psycopg2',
        'HOST': '',
        'PORT': '',
        'DATABASE': '',
        'USER': '',
        'PASSWORD': ''
    }
}
URLS = {
    'city_id': 'http://api.openweathermap.org/data/2.5/find',
    'forecast_day':  'http://api.openweathermap.org/data/2.5/weather'
}
