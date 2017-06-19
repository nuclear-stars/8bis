__author__ = 'Eyal'
from django.conf.urls import url
from . import views

urlpatterns = [
    # Get all restaurants
    url(r'^restaurants/$', views.restaurants, name='restaurants'),

    # Returns all data about a certain restaurant
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/json$', views.rest_detail, name='rest-detail'),
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/today$', views.today_dishes, name='rest-detail'),
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/today/json$', views.today_dishes_json, name='rest-detail-json'),
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/categories/json$', views.get_all_categories, name='get-all-categories'),

    # Get dishes
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/dishes/(?P<dish_id>[0-9]+)/$', views.dish_detail, name='dish-detail'),
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/dishes/add', views.add_dish_to_restaurant, name='add-dish'),
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/dishes/remove', views.remove_dish_from_restuarant, name='remove-dish'),

    # Connect dishes to days
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/dishes/(?P<dish_id>[0-9]+)/set_day$', views.set_day, name='set_day'),
]