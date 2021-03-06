from django.urls import path
from .views import *

app_name = 'bemybaby'

urlpatterns = [
    path('', BeMyBabyAPIView.as_view()),
    path('<int:feed_id>/', BeMyBabyDeletePutView.as_view()),
    path('<int:feed_id>/comments/', BeMyBabyCommentAPIView.as_view()),
    path('comment/<int:comment_id>/', BeMyBabyCommentDeletePutAPIView.as_view()),
]