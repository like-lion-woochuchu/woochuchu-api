from django.urls import path, include
from .views import *

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('', FindMyBabyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:feed_id>/', FindMyBabyDeletePutAPIView.as_view()),
    path('comment/<int:comment_id>/', FindMyBabyCommentDeletePutAPIView.as_view())
]