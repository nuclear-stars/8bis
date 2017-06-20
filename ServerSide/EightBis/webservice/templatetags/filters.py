__author__ = 'Eyal'
from django import template
register = template.Library()

@register.filter(name='getitem')
def getitem(dictionary, key):
    return dictionary.get(key)
