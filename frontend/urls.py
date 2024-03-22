from django.contrib import admin
from django.urls import path, include

from . import views

from SpendScan import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
]