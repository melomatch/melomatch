from urllib.parse import urlencode

from django import template

register = template.Library()


@register.simple_tag
def query_params_link(query_params: dict, **kwargs: dict) -> str:
    return f"?{urlencode(query_params | kwargs, True)}"
