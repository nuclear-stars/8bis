# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Restaurant, Dish, Vote, DishCategory

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Dish)
admin.site.register(Vote)
admin.site.register(DishCategory)