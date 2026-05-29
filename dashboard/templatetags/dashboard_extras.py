import json
from django import template

register = template.Library()


@register.filter
def dict_get(d, key):
    if isinstance(d, dict):
        return d.get(key, {})
    return {}


@register.filter
def dict_get_json(d, key):
    if isinstance(d, dict):
        val = d.get(key, {})
        return json.dumps(val, indent=2)
    return '{}'
