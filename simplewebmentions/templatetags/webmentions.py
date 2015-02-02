from __future__ import unicode_literals, absolute_import

from django import template

from ..models import WebMention

register = template.Library()

@register.assignment_tag
def get_webmentions(path):
    """

    Allows you to get the published Webmentions for a given path
    (i.e. what you get from `my_model_instance.get_absolute_url()`).
    
    ## Usage:

        ```
        {% load webmentions %}
        {% get_webmentions object.get_absolute_url as webmention_list %}
        ```
    
    """
    return WebMention.objects.published().filter(target_path=path)