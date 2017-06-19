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
    restaurant_list = [r.name for r in Restaurant.objects.all()]
    return JsonResponse({'restaurants': restaurant_list})

def rest_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=int(restaurant_id))
    possible_dishes = Dish.objects.filter(restaurant=restaurant.id)
    dishes = [{'name': dish.name,
               'votes': {value[0]: Vote.objects.filter(vote_selection=value).count() for value in Vote.TASTE_VOTES_CHOICES}}
              for dish in possible_dishes]
    value = {
        'name': restaurant.name,
        'dishes': dishes,
    }
    return JsonResponse(value)

def dish_detail(request, dish_id)