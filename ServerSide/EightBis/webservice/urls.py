__author__ = 'Eyal'
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^categories/$', views.get_all_categories, name='get-all-categories'),

    # Get all restaurants
    url(r'^restaurants/$', views.restaurants, name='restaurants'),

    # Returns all data about a certain restaurant
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/$', views.rest_detail, name='rest-detail'),
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/today$', views.today_dishes, name='rest-detail'),

    # Get dishes
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/dishes/(?P<dish_id>[0-9]+)/$', views.dish_detail, name='dish-detail'),
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/dishes/add', views.add_dish_to_restaurant, name='add-dish'),

    # Connect dishes to days
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/dishes/(?P<dish_id>[0-9]+)/set_day$', views.set_day, name='set_day'),
]