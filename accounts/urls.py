from django.contrib import admin
from django.urls import path, include

from accounts.api import LoginAPI, RegisterAPI, UserAPI

urlpatterns = [
    path('login', LoginAPI.as_view()),
    path('signup', RegisterAPI.as_view()),
    path('user', UserAPI)
]