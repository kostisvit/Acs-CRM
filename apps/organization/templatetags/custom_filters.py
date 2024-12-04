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


@register.filter
def username_from_email(value):
    # Check if `value` has an email attribute
    if hasattr(value, 'email'):
        value = value.email
    # Split the email string
    return value.split("@")[0] if isinstance(value, str) and "@" in value else ""