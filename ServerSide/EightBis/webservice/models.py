# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
import json

from django.db import models

class VoteSerializationException(Exception): pass

@python_2_unicode_compatible
class Restaurant(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class DishCategory(models.Model):
    name = models.CharField(max_length=100)

    def get_all_dishes(self):
        """
        :return: All dishes that are in this category
        """
        return Dish.object.filter(category=self.id)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Dish(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    short_desc = models.CharField(max_length=400, null=True)
    recipe = models.CharField(max_length=20000, null=True)

    # Each dish belongs to one category
    category = models.ForeignKey(DishCategory, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    def serialize(self, with_recipe):
        value = {'name': self.name,
               'votes': Vote.get_votes_for_dish_id(self.id),
               'id': self.id,
                'short_desc': self.short_desc}
        if with_recipe:
            value['recipe'] = self.recipe
        return value

    @staticmethod
    def add_dish_from_json(json_encoded, restaurant_id):
        try:
            dish_values = json.loads(json_encoded)
            new_dish = Dish(
                restaurant = Restaurant.objects.get(id=restaurant_id),
                name=dish_values['name'],
                short_desc=dish_values['short_desc'],
                recipe=dish_values['recipe'],
                category=dish_values['category']
            )
            new_dish.save()
        except Exception, e:
            raise VoteSerializationException


################ LEAVING VOTES FOR NOW ##########################
class Vote(models.Model):
    TASTE_VOTES_CHOICES = (
        (u'1', u'Happy'),
        (u'2', u'Vomit'),
        (u'3', u'Bored')
    )
    username = models.CharField(max_length=200)
    vote_time = models.DateField(auto_now=True)
    vote_selection = models.CharField(max_length=1, choices=TASTE_VOTES_CHOICES)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, null=True)

    @staticmethod
    def get_votes_for_dish_id(dish_id):
        return {value[0]: Vote.objects.filter(vote_selection=value[0], dish=dish_id).count()
                for value in Vote.TASTE_VOTES_CHOICES}

    @staticmethod
    def add_vote_from_json(jsoned_vote):
        try:
            vote_values = json.loads(jsoned_vote)
            dish_id = vote_values['dish_id']
            username = vote_values['username']
            vote_selection = vote_values['selection']
        except Exception, e:
            raise VoteSerializationException

        #if Vote.objects.filter(username=username, dish=dish_id, vote_time=models.DateField())

        new_vote = Vote(username=username,
                         dish=Dish.objects.get(id=dish_id),
                         vote_selection=vote_selection)