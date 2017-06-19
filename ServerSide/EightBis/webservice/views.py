# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from .models import Restaurant, Dish, Vote

# Create your views here.
def index(request):
    return HttpResponse("This is my index")

def restaurants(request):
    restaurant_list = [{'name': r.name, 'id': r.id} for r in Restaurant.objects.all()]
    return JsonResponse({'restaurants': restaurant_list})

def rest_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=int(restaurant_id))
    possible_dishes = Dish.objects.filter(restaurant=restaurant.id)
    dishes = [dish.serialize()
              for dish in possible_dishes]
    value = {
        'name': restaurant.name,
        'dishes': dishes,
    }
    return JsonResponse(value)

def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, id=int(dish_id))

    # This means someone is trying to post a review for this meal
    if request.method == 'POST':
        import pdb; pdb.set_trace()

    if request.method == 'GET':
        return JsonResponse(dish.serialize())
