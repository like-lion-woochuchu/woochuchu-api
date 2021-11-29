from django.urls import path
from .views import *

urlpatterns = [
    path('', NoteGetPostAPIView.as_view()),
    path('<int:receiver_id>/', NoteDetailAPIView.as_view())
]