"""
ASGI config for woochuchu project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from decouple import config

SETTINGS = config('SETTINGS')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', SETTINGS)

application = get_asgi_application()
