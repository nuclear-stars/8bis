# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import Restaurant

# Create your views here.
def index(request):
    return HttpResponse("This is my index")

def restaurants(request):
    restaurant_list = [r.name for r in Restaurant.objects.all()]
    return JsonResponse({'restaurants': restaurant_list})
