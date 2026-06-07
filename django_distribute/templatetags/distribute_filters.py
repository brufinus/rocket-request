"""Custom template filters."""

from django import template

register = template.Library()


@register.filter(name="range")
def filter_range(start, end):
    """Returns a python range."""
    try:
        return range(start, end)
    except (TypeError, ValueError):
        return []
