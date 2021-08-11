from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter 

app_name = 'bemybaby'

router = DefaultRouter()
router.register('feed', BeMyBabyFeedViewSet, basename='BeMyBabyFeed')
#router.register('comment', BeMyBabyCommentViewSet, basename='BeMyBabyComment')



urlpatterns = [
    path('<int:pk>/', include(router.urls)),
    path('', include(router.urls)),
    path('feed/<int:id>/comment/', BeMyBabyCommentAPIView.as_view()),
    path('feed/<int:feed_id>/comment/<int:id>/', BeMyBabyCommentDeleteAPIView.as_view()),
]