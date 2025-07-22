from os import getenv

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

APP_HOST = getenv('APP_HOST', '0.0.0.0')
EXTERNAL_PORT = int(getenv('EXTERNAL_PORT', 8080))
INTERNAL_PORT = int(getenv('INTERNAL_PORT', 4000))

SERVICE_NAME = 'cryptocurrency_rates'
PING_ROUTE = getenv('PING_ROUTE', f'/ping/{SERVICE_NAME}')

PYTEST = bool(getenv('PYTEST', False))

POSTGRESQL_HOST = getenv('POSTGRESQL_HOST', '127.0.0.1')
POSTGRESQL_PORT = int(getenv('POSTGRESQL_PORT', 5432))
POSTGRESQL_DATABASE = getenv('POSTGRESQL_DATABASE', 'cryptocurrency_rates')
TEST_POSTGRESQL_DATABASE = getenv('TEST_POSTGRESQL_DATABASE', f'test_{POSTGRESQL_DATABASE}')
POSTGRESQL_USER = getenv('POSTGRESQL_USER', 'postgres')
POSTGRESQL_PASSWORD = getenv('POSTGRESQL_PASSWORD', 'postgres')
POSTGRESQL_MAX_CONNECTIONS = int(getenv('POSTGRESQL_MAX_CONNECTIONS', '5'))

POSTGRES_STR_FOR_CONNECT = (
    f'postgresql+asyncpg://'
    f'{POSTGRESQL_USER}:'
    f'{POSTGRESQL_PASSWORD}@'
    f'{POSTGRESQL_HOST}:'
    f'{POSTGRESQL_PORT}/'
    f'{POSTGRESQL_DATABASE}'
)

DEBUG = bool(getenv('DEBUG', False))
LOGGING_LEVEL = getenv('LOGGING_LEVEL', 'DEBUG')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            'format': '%(asctime)s %(levelname)s %(name)s %(funcName)s %(message)s %(pathname)s %(lineno)s',
        },
        'string': {
            'format': '%(asctime)s %(levelname)s %(name)s %(funcName)s %(message)s %(pathname)s %(lineno)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
            'level': LOGGING_LEVEL,
        },
        'debug_mode': {
            'class': 'logging.StreamHandler',
            'formatter': 'string',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        '': {
            'handlers': ['debug_mode' if DEBUG else 'console'],
            'level': 'DEBUG',
        },
        'aiohttp.access': {
            'level': 'WARNING',
        },
        'logger_sqlalchemy': {
            'level': 'WARN',
            'qualname': 'sqlalchemy.engine',
            'handlers': ['debug_mode' if DEBUG else 'console'],
        },
        'logger_alembic': {
            'level': 'INFO',
            'qualname': 'alembic',
            'handlers': ['debug_mode' if DEBUG else 'console'],
        },
    },
}

BINANCE_BASE_URL = 'https://api.binance.com/api/v3'
