from django import template
import re

register = template.Library()

@register.filter
def remove_protocol(url):
    """
    Removes 'http://' and 'https://' from the start of a URL.
    """
    return re.sub(r'^https?://', '', url)