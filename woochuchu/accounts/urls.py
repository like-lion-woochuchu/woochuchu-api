from django.urls import path
from .views import *

urlpatterns = [
    path('address/', address),
    path('get/', get_address_code),
]