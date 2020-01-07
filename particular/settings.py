from os import environ


ES_HOST = 'localhost:9200'
ES_INDEX = 'particular-pages'

SECRET_KEY = environ['SECRET_KEY']

ENV = environ.get('ENV', 'dev')


# Env settings
#

DEBUG = ENV == 'dev'

if ENV == 'production':
    SEARCH_URL = 'https://particular.fizzadar.com'
    ADMIN_URL = 'https://particular-admin.fizzadar.com'
else:
    SEARCH_URL = 'http://localhost:5000'
    ADMIN_URL = 'http://localhost:5001'
