# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import datetime
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from .models import Restaurant, Dish, Vote, VoteSerializationException, DishCategory, \
                    DailyDish

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
        return JsonResponse(dish.serialize(with_recipe=False))

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

def remove_dish_from_restuarant(request, restaurant_id):
    """
    removes a dish from the list of dishes for a certain restaurant
    """
    result = {'result': 'False'}
    try:
        json_content = request.read()
        dish = Dish.object.get(id=json_content['id'])
        dish.delete()
    except Exception, e:
        pass
    return JsonResponse(result)

@csrf_exempt
def set_day(request, restaurant_id, dish_id):
    """
    Add this certain dish to the list of dishes for a certain day
    for this restaurant
    """
    result = {'result': 'False'}
    if request.method == "POST":
        try:
            restaurant = get_object_or_404(Restaurant, id=restaurant_id)
            dish = get_object_or_404(Dish, id=dish_id)
            json_content = json.loads(request.read())
            if json_content['day'] == 'today':
                now = datetime.datetime.now()

                # Make sure this dish doesn't already exist in that days dishes
                if DailyDish.objects.filter(dish=dish_id, day__day=now.day, day__year=now.year, day__month=now.month).count() == 0:
                    new_daily = DailyDish(dish=dish,
                                          restaurant=restaurant,
                                          extra_recipe="",
                                          day=now)
                    new_daily.save()
                    result = {'result': "True"}
        except Exception, e:
            import pdb; pdb.set_trace()
    return JsonResponse(result)


def get_today_dishes_as_dict(restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=int(restaurant_id))
    # Get the list of dishes that are associated for today
    today = datetime.datetime.now()
    daily_dishes = DailyDish.objects.filter(restaurant=restaurant.id, day__day=today.day,
                                            day__year=today.year,
                                            day__month=today.month)

    categories = {}
    for dish in daily_dishes:
        d = categories.get(dish.dish.category.name, [])
        d.append({
            'name': dish.dish.name,
            'short_desc': dish.dish.short_desc,
            'recipe': dish.dish.recipe,
            'category_id': dish.dish.category.id,
            'extra_recipe': dish.extra_recipe,
        })
        categories[dish.dish.category.name] = d

    return categories


def today_dishes(request, restaurant_id):
    context = {'today_date': datetime.datetime.now().strftime("%d.%m.%y"),
               'categories': get_today_dishes_as_dict(restaurant_id)}
    return render(request, 'webservice/menu.html', context)


def today_dishes_json(request, restaurant_id):
    return JsonResponse(get_today_dishes_as_dict(restaurant_id))


def get_all_categories(request, restaurant_id):
    all_cats = DishCategory.objects.all()
    value = {'categories': {
        'id': cat.id,
        'name': cat.name
    } for cat in all_cats}
    return JsonResponse(value)

