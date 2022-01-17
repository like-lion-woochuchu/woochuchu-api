from django.urls import path
from .views import *

app_name = 'mybaby'

urlpatterns = [
    path('', MyBabyAPIView.as_view()),
    path('<int:feed_id>/', MyBabyDeletePutView.as_view()),
    path('<int:feed_id>/comments/', MyBabyCommentAPIView.as_view()),
    path('comment/<int:comment_id>/', MyBabyCommentDeletePutAPIView.as_view()),
    path('<int:feed_id>/likes/', MyBabyLikeAPIView.as_view()),
]