"""

DailyRounds App Settings or Configuration

"""

SECRET_KEY = "dTXgY7*uzDCawUMp+3xqp-nG!DvFRvz7rYw6Q2+cTC_j+hQ43mt&?Zub#2?N"
DEBUG = False
GLOBAL_PAGE_SIZE = 5
TOKEN_GEN_SEC_KEY = "eyJfaWQiOiI1NWM0M2VlN2JjYzQzNDBiN2Y4ZGNkZjnayr_YOnqZMI"
TOKEN_GEN_SEC_SALT_KEY = "eyJfaWQiOiI1NWRhY2M1Y2Jj06T7PG3uCZaDXV2SmoV8J8HAqU"
REF_SECRET_KEY = "sadladpipo36Mp+3xqp-nG!DvFRvz7rYw6Q2+cTC_j+hQ43mt&?Zub#2?N"
APP_PWD_SALT = 'u9F6j#Bp8WuWq&5y&Du2+b+2S8yW+L'
API_VERSION = "v1"
LOG_FOLDER = '/tmp/logs'
DOMAIN = "localhost:8080"
PAGINATION = {
    'default': {
        'skip': 0,
        'limit': 5,
        'max_skip': 0,
        'max_limit': 50,
    }
}

MONGO = [{
    "host": "127.0.0.1",
    "port": 27017,
    "db": "api_db",
    "is_replica": False,
    "replica_sets": [],
    "replica_set_name": ""
}]
