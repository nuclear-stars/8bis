__author__ = 'Eyal'
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^restaurants', views.index, name='restaurants'),
]