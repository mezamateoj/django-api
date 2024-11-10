from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# registering viewset views
router = DefaultRouter()
router.register('api/hello-viewset', views.HelloViewSet, basename='hello-viewset')

urlpatterns = [
    path('api/hello', views.HelloView.as_view(), name='hello-view'),
    path('', include(router.urls))
]
