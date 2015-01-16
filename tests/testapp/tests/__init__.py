from __future__ import absolute_import

from simplewebmentions.models import WebMention
from django.contrib.contenttypes.models import ContentType
from ..models import BlogPost

CT = ContentType.objects.get_for_model

from .webmention_views import *