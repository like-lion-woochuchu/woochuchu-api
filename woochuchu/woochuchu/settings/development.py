from woochuchu.settings.base import *

DEBUG = True

ALLOWED_HOSTS = ["7f0b-220-76-68-249.ngrok.io"]

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


CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True