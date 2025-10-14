# custom_filters.py
from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, class_name):
    """
    Adds a CSS class to a form field widget.
    """
    return value.as_widget(attrs={'class': class_name})
