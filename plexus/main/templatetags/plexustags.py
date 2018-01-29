from django import template

from plexus.main.models import Application

register = template.Library()


@register.simple_tag
def app_by_graphite_name(name):
    try:
        return Application.objects.get(graphite_name=name)
    except Application.DoesNotExist:
        return None
