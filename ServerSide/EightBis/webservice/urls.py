__author__ = 'Eyal'
from django.conf.urls import url
from . import views

urlpatterns = [
    # Get all restaurants
    url(r'^restaurants/$', views.restaurants, name='restaurants'),

    # Returns all data about a certain restaurant
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/json$', views.rest_detail, name='rest-detail'),
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/today$', views.today_dishes, name='rest-detail'),
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/(?P<day>\d{4}-\d{2}-\d{2})/$', views.day_dishes, name='rest-detail-day'),

    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/today/json$', views.today_dishes_json, name='rest-detail-json'),
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/(?P<day>\d{4}-\d{2}-\d{2})/json$', views.dishes_per_day_json, name='rest-detail-json'),
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/today/print.html', views.today_dishes_print, name='rest-detail-print-today'),
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/(?P<day>\d{4}-\d{2}-\d{2})/print.html', views.dishes_print, name='rest-detail-print'),
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/categories/json$', views.get_all_categories, name='get-all-categories'),

    # Get dishes
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/dishes/(?P<dish_id>[0-9]+)/$', views.dish_detail, name='dish-detail'),
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/dishes/add', views.add_dish_to_restaurant, name='add-dish'),
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/dishes/remove', views.remove_dish_from_restuarant, name='remove-dish'),
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/dishes/(?P<dish_id>[0-9]+)/update$', views.dish_update, name='dish-update'),

    # Connect dishes to days
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/dishes/(?P<dish_id>[0-9]+)/set_day$', views.set_day, name='set_day'),
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/dishes/(?P<dish_id>[0-9]+)/unset_day$', views.unset_day, name='set_day'),
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/dishes/(?P<dish_id>[0-9]+)/set_extra_recipe$', views.set_extra_recipe, name='set_extra_recipe'),

    # Manage UI
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/manage/$', views.manage_view, name='rest-manage-view'),
    url(r'^restaurants/(?P<restaurant_id>[0-9]+)/manage/statistics/$', views.satistics_view, name='rest-manage-statistics'),
]