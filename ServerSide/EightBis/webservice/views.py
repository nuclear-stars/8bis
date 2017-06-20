# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import datetime
import time
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

@csrf_exempt
def dish_update(request, restaurant_id, dish_id):
    dish = get_object_or_404(Dish, id=int(dish_id))
    restaurant = get_object_or_404(Restaurant, id=int(restaurant_id))

    result = {'result': 'False'}
    try:
        values = json.loads(request.read())
        dish.recipe = values['recipe']
        dish.name = values['name']
        dish.short_desc = values['short_desc']
        dish.save()
        result = {'result': 'True'}
    except Exception, e:
        pass
    return JsonResponse(result)

# restaurants/(?P<restaurant_id>[0-9]+)/dishes/(?P<dish_id>[0-9]+)/$
@csrf_exempt
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
        return JsonResponse({'result': 'True'})

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
                date = datetime.datetime.now()
            else:
                date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(json_content['day'], "%Y-%m-%d")))

            # Make sure this dish doesn't already exist in that days dishes
            if DailyDish.objects.filter(dish=dish_id, day__day=date.day, day__year=date.year, day__month=date.month).count() == 0:
                new_daily = DailyDish(dish=dish,
                                      restaurant=restaurant,
                                      extra_recipe="",
                                      day=date)
                new_daily.save()
                result = {'result': "True"}
        except Exception, e:
            pass
    return JsonResponse(result)

@csrf_exempt
def set_extra_recipe(request, restaurant_id, dish_id):
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
                date = datetime.datetime.now()
            else:
                date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(json_content['day'], "%Y-%m-%d")))

            # Check if this dish is already set, if not we can't add a recepie
            daily_dish = DailyDish.objects.filter(dish=dish_id, day__day=date.day, day__year=date.year, day__month=date.month)
            if len(daily_dish) != 0:
                new_daily = daily_dish[0]
                new_daily.extra_recipe = json_content['extra_recipe']
                new_daily.save()

                result = {'result': "True"}
        except Exception, e:
            pass
    return JsonResponse(result)


@csrf_exempt
def unset_day(request, restaurant_id, dish_id):
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
                date = datetime.datetime.now()
            else:
                date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(json_content['day'], "%Y-%m-%d")))

                # Make sure this dish doesn't already exist in that days dishes
                dish = DailyDish.objects.filter(dish=dish_id, day__day=date.day, day__year=date.year, day__month=date.month)
                if len(dish) > 0:
                    dish.delete()
                    result = {'result': 'True'}

        except Exception, e:
            pass
    return JsonResponse(result)


def get_day_dishes_as_dict(restaurant_id, day):
    restaurant = get_object_or_404(Restaurant, id=int(restaurant_id))
    # Get the list of dishes that are associated for today
    daily_dishes = DailyDish.objects.filter(restaurant=restaurant.id, day__day=day.day,
                                            day__year=day.year,
                                            day__month=day.month)

    categories = {}
    for dish in daily_dishes:
        d = categories.get(dish.dish.category.name, [])

        recipe = dish.dish.recipe
        if dish.extra_recipe is not None and len(dish.extra_recipe) > 0:
            recipe = dish.extra_recipe
        d.append({
            'name': dish.dish.name,
            'short_desc': dish.dish.short_desc,
            'recipe': recipe,
            'category_id': dish.dish.category.id,
            'id': dish.dish.id
        })
        categories[dish.dish.category.name] = d

    return categories


def get_today_dishes_as_dict(restaurant_id):
    today = datetime.datetime.now()
    return get_day_dishes_as_dict(restaurant_id, today)

def get_dishes_as_list_per_day(restaurant_id, day):
    category_to_dish = get_day_dishes_as_dict(restaurant_id, day)
    result_list = []
    for cat, dishes in category_to_dish.items():
         for dish in dishes:
             result_list.append(dish)
    return result_list

def get_today_dishes_as_list(restaurant_id):
    category_to_dish = get_today_dishes_as_dict(restaurant_id)
    result_list = []
    for cat, dishes in category_to_dish.items():
         for dish in dishes:
             result_list.append(dish)
    return result_list

@csrf_exempt
def today_dishes(request, restaurant_id):
    # Get means user hasn't authenticated yet.
    if request.method == 'GET':
        return render(request, 'webservice/login.html', {})

    # Verify username is not malicious
    username = request.POST.get("Username")

    dishes_dict = get_today_dishes_as_dict(restaurant_id)
    votes_dict = {dish['id']: Vote.get_votes_for_dish_id(dish['id']) for cat in dishes_dict.values() for dish in cat}
    context = {
               'today_date': datetime.datetime.now().strftime("%d.%m.%y"),
               'categories': dishes_dict,
               'votes': votes_dict,
               'vote_choices': Vote.TASTE_VOTES_CHOICES,
                'username': username
               }
    return render(request, 'webservice/menu.html', context)

def today_dishes_print(request, restaurant_id):
    dishes_dict = get_today_dishes_as_dict(restaurant_id)
    context = {
        'today_date': datetime.datetime.now().strftime("%d.%m.%y"),
        'categories': dishes_dict,
    }
    return render(request, 'webservice/printable_menu.html', context)

def dishes_per_day_json(request, restaurant_id, day):
    # Convert the value of the day
    try:
        day = datetime.datetime.fromtimestamp(time.mktime(time.strptime(day, "%Y-%m-%d")))
    except Exception, e:
        return JsonResponse({"result": "False"})
    value = {'dishes': get_dishes_as_list_per_day(restaurant_id, day=day)}
    return JsonResponse(value)


def today_dishes_json(request, restaurant_id):
     value = {'dishes': get_today_dishes_as_list(restaurant_id)}
     return JsonResponse(value)


def get_all_categories(request, restaurant_id):
    all_cats = DishCategory.objects.all()
    value = {'categories': {
        cat.id: cat.name  for cat in all_cats
    }}
    return JsonResponse(value)

