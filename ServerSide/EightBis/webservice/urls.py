__author__ = 'Eyal'
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^categories', views.get_all_categories, name='get-all-categories'),

    url(r'^restaurants', views.restaurants, name='restaurants'),
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/$', views.rest_detail, name='rest-detail'),

    # Get dishes
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/dishes/(?P<dish_id>[0-9]+)/$', views.dish_detail, name='dish-detail'),
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/dishes', views.add_dish_to_restaurant, name='add-dish')
]