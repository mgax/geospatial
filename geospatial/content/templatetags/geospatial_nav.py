from django import template

from geospatial.content.models import HomePage

register = template.Library()


@register.simple_tag()
def get_nav_pages():
    homepage = HomePage.objects.get()
    return homepage.get_children().live().in_menu()
