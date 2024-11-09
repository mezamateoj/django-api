from django.urls import path

from . import views

urlpatterns = [
    path('api/profile', views.Profile.as_view(), name='create-profile'),
]
