"""
TODO: send relevant signals when creating, deleting, unpublishing etc...

TODO: How to best connect various bit that we can read from the URLs?

"""

from __future__ import unicode_literals
from urlparse import urlparse

from webmentiontools.urlinfo import UrlInfo

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseNotAllowed
from django.core.urlresolvers import resolve, reverse
from django.shortcuts import render_to_response
from django.views.generic import View, DetailView
from django.views.defaults import bad_request
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from simplewebmentions.helpers import (
    verify_params, is_valid_target, get_source_data,
    mention_status_check, delete_if_existing, get_article_text)
from simplewebmentions.models import (
    WebMention, MENTION_STATUS_UNMODERATED, MENTION_STATUS_DELETED)


class WebMentionDetail(View):
    
    def dispatch(self, request, *args, **kwargs):
        allowed_methods = ['GET', 'HEAD']
        if request.method not in allowed_methods:
            return HttpResponseNotAllowed(allowed_methods)
        mention = get_object_or_404(WebMention, **kwargs)
        message, status = mention_status_check(mention)  
        return HttpResponse(message, status=status)


class WebMentionEndpoint(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(WebMentionEndpoint, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Doing a get request should return a nice overview HTML page.
        """
        response = render_to_response('webmentions/webmention_endpoint.html')
        response.Link = reverse('webmention_endpoint')
        return response

    
    def post(self, request, *args, **kwargs):
        """
        Handles post requests to our endpoint. Should check parameters
        and trigger WebMention creation if present and correct.
        """

        if not verify_params(request.POST):
            return bad_request(request)

        target = request.POST['target']
        source = request.POST['source']

        
        match = is_valid_target(target, request)
        # Does the target exist on the site, and is there a source to parse?
        if not match:
            """
            If there doesn't seem to be content representing the target,
            the webmention is rejected.
            """
            delete_if_existing(source, target)
            return bad_request(request)

        # Use webmention-tools to try and fetch/parse the source
        source_data = get_source_data(source)

        # Is there some source data to parse?
        if source_data.error:
            """
            The source data could not be parsed by webmention-tools,
            webmention is rejected.
            """
            delete_if_existing(source, target)
            return bad_request(request)

        if not source_data.linksTo(target):
            """
            If the source page does not contain a link back to the target,
            the mention is rejected.
            """
            delete_if_existing(source, target)
            return bad_request(request)

        target_app = match.app_name

        mention = WebMention(
            source=source,
            target=target,
            source_title=source_data.title(),
            target_app=target_app or "",
            source_link_excerpt=source_data.snippetWithLink(source_data.url) or "",
            source_pub_date=source_data.pubDate(),
            author_img_url=source_data.image() or "",
            source_text=get_article_text(source_data.soup)
            )

        mention.save()

        return HttpResponse(mention.get_absolute_url(), status=202)


    def head(self, request, *args, **kwargs):
        """
        Basically, disallow HEAD requests to the endpoint.
        """
        return HttpResponseNotAllowed(['POST', 'GET'])

