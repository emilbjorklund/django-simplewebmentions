from __future__ import absolute_import
from django.http import HttpResponse
from simplewebmentions.helpers import is_valid_target


def dummy_webmention(request, *args, **kwargs):
    match = is_valid_target(target, request)
    if match:
        return HttpResponse('webmention allowed', status=200)
    