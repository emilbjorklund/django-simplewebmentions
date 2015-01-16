"""
TODO: send relevant signals when creating, deleting, unpublishing etc...

TODO: How to best connect various bit that we can read from the URLs?

"""

from __future__ import unicode_literals
from urlparse import urlparse

from webmentiontools.urlinfo import UrlInfo

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseNotAllowed
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
from django.views.generic import View, DetailView
from django.views.defaults import bad_request
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from simplewebmentions.models import (
    WebMention, MENTION_STATUS_UNMODERATED, MENTION_STATUS_DELETED)


class WebMentionDetail(View):
    
    def dispatch(self, request, *args, **kwargs):
        if request.method not in ['GET', 'HEAD']:
            return bad_request(request)
        mention = get_object_or_404(WebMention, **kwargs)
        if mention.is_public:
            status = 200  # OK
        if mention.status == MENTION_STATUS_UNMODERATED:
            status = 202  # received
        if mention.status == MENTION_STATUS_DELETED:
            status = 410  # gone
        return HttpResponse('<p>Mention for: ' + mention.target + '</p><p>Status: %s</p>' % status, status=status)


class WebMentionEndpoint(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(WebMentionEndpoint, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Doing a get request should return a nice overview HTML page.
        """
        return render_to_response('webmentions/webmention_endpoint.html')

    
    def post(self, request, *args, **kwargs):
        """
        Handles post requests to our endpoint. Should check parameters
        and trigger WebMention creation if present and correct.
        """

        # Post must contain `target` and `source` parameters:
        if ('target' not in request.POST) or ('source' not in request.POST):
            return bad_request(request)

        target = request.POST['target']
        source = request.POST['source']

        # Use webmention-tools to try and fetch/parse the source
        source_data = UrlInfo(source)
        match = existing_target(target, request)
        # Does the target exist on the site, and is there a source to parse?
        if not match:
            """
            If there doesn't seem to be content representing the target,
            the webmention is rejected.
            """
            delete_if_existing(source)
            return bad_request(request)

        # Is there some source data to parse?
        if source_data.error:
            """
            The source data could not be parsed by webmention-tools,
            webmention is rejected.
            """
            delete_if_existing(source)
            return bad_request(request)

        if not source_data.linksTo(target):
            """
            If the source page does not contain a link back to the target,
            the mention is rejected.
            """
            delete_if_existing(source)
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


def existing_target(url, request):
    """
    Take a URL string and check if the path component
    seems to exist on the current site.
    Returns False if the URL raises a 404, and a UrlResolver object
    if the URL seems to exist.
    """
    parsed = urlparse(url)
    
    try:
        match = resolve(parsed.path)
        kwargs = match.kwargs
        args = match.args
        kwargs['request'] = request
        match.func(*args, **kwargs)
    except Http404:
        return False
    return match


def get_article_text(soup):
    """
    Get some sort of reasonable representation of the main text of the
    BeautifulSoup instance (soup parameter).
    """
    # MF2
    article = soup.find(True, attrs={'class':'h-entry'}).find(True, attrs={'class': 'e-content'})
    if not article:
        article = soup.find(True, attrs={'class':'hentry'}).find(True, attrs={'class': 'entry-body'})
    if not article:
        return ""
    return article


def delete_if_existing(source_url):
    """
    If a mention fails for some reason, any reference to that mention
    should be deleted/marked as deleted.
    """
    mentions = Mention.objects.filter(source=source_url)
    for mention in mentions:
        mention.status = MENTION_STATUS_DELETED
        mention.save()
