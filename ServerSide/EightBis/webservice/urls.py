__author__ = 'Eyal'
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/$', views.rest_detail, name='rest-detail'),
    url(r'^restaurants', views.restaurants, name='restaurants'),
    url(r)
]