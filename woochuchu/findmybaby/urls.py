from django.urls import path
from .views import *

urlpatterns = [
    path('', FindMyBabyAPIView.as_view()),
    path('<int:feed_id>/', FindMyBabyDetailAPIView.as_view()),
    path('<int:feed_id>/comments/', FindMyBabyCommentAPIView.as_view()),
    path('comment/<int:comment_id>/', FindMyBabyCommentDeletePutAPIView.as_view())
]