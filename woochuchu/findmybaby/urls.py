from django.urls import path, include
from .views import *

urlpatterns = [
    path('', FindMyBabyAPIView.as_view()),
    path('<int:feed_id>/', FindMyBabyDeletePutAPIView.as_view()),
    path('<int:feed_id>/comments/', FindMyBabyCommentAPIView.as_view()),
    path('comment/<int:comment_id>/', FindMyBabyCommentDeletePutAPIView.as_view())
]