import json
from django import template

register = template.Library()

@register.filter(name='json')
def json_filter(value, indent=4):
    return json.dumps(value, indent=indent)
