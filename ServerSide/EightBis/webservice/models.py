# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models

@python_2_unicode_compatible
class Restaurant(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Dish(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    def serialize(self):
        return {'name': self.name,
               'votes': Vote.get_votes_for_dish_id(self.id),
               'id': self.id}

class Vote(models.Model):
    TASTE_VOTES_CHOICES = (
        (u'1', u'Happy'),
        (u'2', u'Vomit'),
        (u'3', u'Bored')
    )
    username = models.CharField(max_length=200)
    vote_time = models.DateField()
    vote_selection = models.CharField(max_length=1, choices=TASTE_VOTES_CHOICES)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, null=True)

    @staticmethod
    def get_votes_for_dish_id(dish_id):
        return {value[0]: Vote.objects.filter(vote_selection=value[0], dish=dish_id).count()
                for value in Vote.TASTE_VOTES_CHOICES}