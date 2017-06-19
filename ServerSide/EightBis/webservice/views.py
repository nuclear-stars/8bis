# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from .models import Restaurant, Dish, Vote, VoteSerializationException, DishCategory

# Create your views here.
def index(request):
    return HttpResponse("This is my index")

def restaurants(request):
    restaurant_list = [{'name': r.name, 'id': r.id} for r in Restaurant.objects.all()]
    return JsonResponse({'restaurants': restaurant_list})

# restaurants/(?P<restaurant_id>[0-9]+)/$
def rest_detail(request, restaurant_id):
    """
    Returns all possible dishes for a restaurant
    """
    restaurant = get_object_or_404(Restaurant, id=int(restaurant_id))
    possible_dishes = Dish.objects.filter(restaurant=restaurant.id)
    dishes = [dish.serialize(with_recipe=True)
              for dish in possible_dishes]
    value = {
        'name': restaurant.name,
        'dishes': dishes,
    }
    return JsonResponse(value)

# restaurants/(?P<restaurant_id>[0-9]+)/dishes/(?P<dish_id>[0-9]+)/$
def dish_detail(request, restaurant_id, dish_id):
    dish = get_object_or_404(Dish, id=int(dish_id))

    # This means someone is trying to post a review for this meal
    if request.method == 'POST':
        try:
            request_content = request.read()
            Vote.add_vote_from_json(request_content)
        except VoteSerializationException, e:
            # This means the user sent a melformed json
            return HttpResponse('Wrong JSON format', status=204)

    if request.method == 'GET':
        return JsonResponse(dish.serialize())

# restaurants/(?P<restaurant_id>[0-9]+)/dishes
def add_dish_to_restaurant(request, restaurant_id):
    """
    Adds a new dish to the menu
    """
    # Adding a new dish is a post method with a json that contains all values
    if request.method == 'POST':
        result = {'result': 'True'}
        try:
            json_content = request.read()
            Dish.add_dish_from_json(json_content, restaurant_id)
        except VoteSerializationException:
            result = {'result': 'False'}
        return JsonResponse(result)

def get_all_categories(request):
    all_cats = DishCategory.objects.all()
    value = {'categories': {
        'id': cat.id,
        'name': cat.name
    } for cat in all_cats}
    return JsonResponse(value)

