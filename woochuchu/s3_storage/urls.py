from django.urls import path
from .views import *

app_name = 's3_storage'

urlpatterns = [
    path('', ImageUploadDeleteAPIView.as_view())
]
