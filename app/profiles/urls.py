from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('profile-view', views.ProfileViewSet)
router.register('feed', views.UserProfileFeedViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # This will prefix all router URLs with 'api/'
    path('api/profile/', views.Profile.as_view(), name='create-profile'),
    path('api/token/', views.UserLoginApiView.as_view(), name='create-token'),
]
