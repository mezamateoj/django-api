from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
# dont need basename because we are using queryset on the view
router.register('api/profile-view', views.ProfileViewSet)

urlpatterns = [
    path('api/profile', views.Profile.as_view(), name='create-profile'),
    path('', include(router.urls)),
]
