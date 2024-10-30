from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})

@register.filter(name='truncate_words')
def truncate_words(value, args):
    if len(value) > args:
        return value[:args] + '...'
    return value