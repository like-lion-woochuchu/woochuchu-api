from woochuchu.settings.base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

LOGGING = {
    'version' : 1,
    'disable_existing_loggers': False,
    'handlers' : {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}