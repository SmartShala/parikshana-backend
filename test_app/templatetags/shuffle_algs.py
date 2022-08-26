# app/templatetags/shuffle.py
import random
from django import template

register = template.Library()


def shuffle(var, arg):
    print(var)
    tmp = list(var)[:]
    random.Random(arg).shuffle(tmp)
    return tmp


def to_char(value):
    return chr(64 + value)


register.filter("shuffle", shuffle)
register.filter("to_char", to_char)
