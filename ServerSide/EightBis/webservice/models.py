# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
import json
import datetime

from django.db import models

class VoteSerializationException(Exception): pass

@python_2_unicode_compatible
class Restaurant(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
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
                'short_desc': self.short_desc,
                 'category': self.category.id}
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

@python_2_unicode_compatible
class DailyDish(models.Model):
    """
    Represents one connection of a meal to a day
    """
    dish = models.ForeignKey(Dish)
    day = models.DateField()
    extra_recipe = models.CharField(max_length=2000, null=True)
    restaurant = models.ForeignKey(Restaurant)

    def __str__(self):
        return self.dish.name + " @ " + str(self.day)

@python_2_unicode_compatible
class Vote(models.Model):
    TASTE_VOTES_CHOICES = (
        (u'1', (u'טעים!', u'tasty', u'😍')),
        (u'2', (u'לא משהו', u'disliked', u'😣')),
        (u'3', (u'בריא', u'healthy', u'🌿')),
        (u'4', (u'שמן', u'fat', u'🍔')),
        (u'5', (u'מפתיע!', u'surprising', u'🌟')),
        (u'6', (u'לא נשאר לי', u'none-left', u'🛑')),
    )
    username = models.CharField(max_length=200)
    vote_time = models.DateField()
    vote_selection = models.CharField(max_length=1)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, null=True)

    @staticmethod
    def get_votes_for_dish_id(dish_id):
        return {value[0]: Vote.objects.filter(vote_selection=value[0], dish=dish_id).count()
                for value in Vote.TASTE_VOTES_CHOICES}

    def __str__(self):
        return "Vote: {selection} On {dish} by {user}".format(selection=self.vote_selection, dish=self.dish.name,
                                                               user=self.username)

    @staticmethod
    def get_diners_per_day(day):
        return Vote.objects.filter(vote_time=day).order_by().values("username").distinct().count()

    @staticmethod
    def add_vote_from_json(jsoned_vote):
        try:
            vote_values = json.loads(jsoned_vote)
            dish_id = vote_values['dish_id']
            username = vote_values['username']
            vote_current_state = vote_values['votes']

            # First we check if this user has already voted for this dish
            previous_opinions = Vote.objects.filter(dish=dish_id, username=username)
            previous_opinion_vector = {}
            for key in Vote.TASTE_VOTES_CHOICES:
                if any(map(lambda x: x.vote_selection == key[0], previous_opinions)):
                    previous_opinion_vector[key[0]] = True
                else:
                    previous_opinion_vector[key[0]] = False

            # Go over all vote options and see if we need to change the state
            for key in previous_opinion_vector.keys():
                # Check if the user has revoked his selection
                if previous_opinion_vector[key] and not vote_current_state[key]:
                     previous_opinions.filter(vote_selection=key).delete()
                if not previous_opinion_vector[key] and vote_current_state[key]:
                     new_vote = Vote(username=username,
                                     dish=Dish.objects.get(id=dish_id),
                                     vote_selection=key,
                                     vote_time=datetime.datetime.now())

                     new_vote.save()

        except Exception, e:
            raise VoteSerializationException


