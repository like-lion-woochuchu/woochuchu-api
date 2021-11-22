from django.urls import path
from .views import *

urlpatterns = [
    path('', NotePostAPIView.as_view()),
    path('<str:user_uuid>/', NoteListAPIView.as_view())
]