from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter 

app_name = 'bemybaby'

urlpatterns = [
    path('', BeMyBabyFeedView.as_view()),
    path('<int:feed_id>/', BeMyBabyFeedDetailView.as_view()),
    path('<int:feed_id>/comment/', BeMyBabyCommentAPIView.as_view()),
    path('comment/<int:comment_id>/', BeMyBabyCommentDetailAPIView.as_view()),
]