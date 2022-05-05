from django import template
from django.urls import resolve

from blog.models import BlogCategory

register = template.Library()


@register.inclusion_tag('blog/categories.html', takes_context=True)
def show_categories(context):
    category = context.request.GET.get("category")
    current_url = context.request.path_info
    in_home = False
    if 'blog' in current_url and not current_url.split('/')[2]:
        in_home = True
    categories = BlogCategory.objects.all()
    return {'categories': categories, 'current_url': current_url, "in_home": in_home}