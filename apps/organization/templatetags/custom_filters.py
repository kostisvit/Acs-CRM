from django import template
import re

register = template.Library()

@register.filter
def remove_protocol(url):
    """
    Removes the 'http://' and 'https://' protocols from a URL.
    """
    if not url:
        return url
    return re.sub(r'^https?://', '', url)
