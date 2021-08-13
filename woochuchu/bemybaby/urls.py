from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter 

app_name = 'bemybaby'

router = DefaultRouter()
router.register('', BeMyBabyFeedViewSet, basename='BeMyBabyFeed')
#router.register('comment', BeMyBabyCommentViewSet, basename='BeMyBabyComment')



urlpatterns = [
    path('', include(router.urls)),
    path('<int:feed_id>/comment/', BeMyBabyCommentAPIView.as_view()),
    path('<int:feed_id>/comment/<int:id>/', BeMyBabyCommentDeleteAPIView.as_view()),
]