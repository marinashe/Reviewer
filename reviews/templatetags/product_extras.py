from django import template

register = template.Library()


@register.filter
def full_stars(value):
    return '*' * int(value)


@register.filter
def empty_stars(value):
    return '*' * (10 - int(value))
