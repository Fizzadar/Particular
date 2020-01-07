from os import environ, getcwd, path

from particular.settings import (  # noqa: F401
    ADMIN_URL,
    DEBUG,
    ENV,
    ES_INDEX,
    SEARCH_URL,
    SECRET_KEY,
)


PARTICULAR_STATIC_DIR = path.join(getcwd(), 'particular', 'static')

AUTH_TOKEN_EXPIRE_SECONDS = 900

USER_LEVEL = 1
MODERATOR_LEVEL = 5
ADMIN_LEVEL = 9
KEYMASTER_LEVEL = 10

HASH_IDS_MIN_LENGTH = 6

WEBSITE_HASH_IDS_SALT = environ['WEBSITE_HASH_IDS_SALT']

MAILGUN_FROM_ADDRESS = "Fizzadar's Particular <pointlessrambler@gmail.com>"
MAILGUN_DOMAIN = 'mail.particular.fizzadar.com'

MAILGUN_API_KEY = environ['MAILGUN_API_KEY']

DATABASE = {
    'NAME': 'particular',
    'HOST': 'localhost',
    'PORT': 3306,
    'USER': environ['DATABASE_USER'],
    'PASSWORD': environ['DATABASE_PASSWORD'],
}
