"""
Utility functions for handling Webmention data.
"""

from functools import wraps

from webmentiontools.urlinfo import UrlInfo

from django.utils.six.moves.urllib import parse as urlparse
from django.utils.decorators import available_attrs
from django.core.urlresolvers import resolve, is_valid_path
from django.http import Http404
from django.conf import settings

from simplewebmentions.models import (
    WebMention, MENTION_STATUS_UNMODERATED, MENTION_STATUS_DELETED)


def verify_params(post_dict):
    """
    Verify that a post dict contains the expected parameters.
    """
    if ('target' not in post_dict) or ('source' not in post_dict):
        return False
    if not post_dict['target'] or not post_dict['source']:
        return False
    return True


def is_valid_target(url, request):
    """
    Take a URL string and check if the path component
    seems to exist on the current site.
    Returns False if the URL raises a 404, and a UrlResolver object
    if the URL seems to exist.
    """

    # First, set up a variable for the tentative status:
    accepts_webmentions = False

    # Parse the URL into its components:
    parsed = urlparse(url)
    
    # Run a try/catch to see if such a path would ultimately raise a 404:
    try:
        """
        If the parsed path is valid, `match` becomes a dict with
        info on the view. This is done by running a resolver on the path.
        """

        # Try to match the path:
        match = resolve(parsed.path)
        # First, check if this view accepts webmentions via decorator.
        if match and match.func.accepts_webmentions:
            accepts_webmentions = True

        # If not, there may be a registry of webmention paths that tells you:
        if not accepts_webmentions:
            # TODO: Check the registry
            pass

        # Pass on the args/keyword args
        kwargs = match.kwargs
        args = match.args

        # Augment the keyword arguments with the request, to be able to
        # try and call it.
        kwargs['request'] = request

        match.func(*args, **kwargs)
    except Http404:
        return False
    return match


def get_source_data(source):
    """
    Parse the source and return various bits of data from that page.
    For now, uses webmention-tools to do this.
    """
    return UrlInfo(source)


def delete_if_existing(request, source_url, target_url):
    """
    If a mention fails for some reason, any reference to that mention
    should be deleted/marked as deleted.
    """
    mentions = WebMention.objects.filter(source=source_url, target=target_url)
    
    for mention in mentions:
        if is_valid_referrer(request, mention, settings.ALLOWED_HOSTS):
            mention.status = MENTION_STATUS_DELETED
            mention.save()

def mention_status_check(mention):
    if mention.is_public:
        status = 200  # OK
    if mention.status == MENTION_STATUS_UNMODERATED:
        status = 202  # received
    if mention.status == MENTION_STATUS_DELETED:
        status = 410  # gone
    return (
        '<p>Mention for: %s</p><p>Status: %s</p>' % (mention.source, status),
        status)


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

# Not sure if this is even useful.
def is_valid_referrer(request, mention, own_valid_hosts):
    """
    Check if the mention comes from
    a) your own sites (e.g. sites in allowed apps or localhost)
    b) the host from the same URL as sent the webmention.
    """
    source_host = urlparse(mention.source).hostname
    host = request.get_host()
    valid = valid_hosts + (host,) 
    return (host in valid)


def accept_webmentions(view):
    """
    Decorator for view functions, to allow you to determine if the view
    as a whole accepts Webmentions (in cases where you don't) want to or
    can't use a registry of paths to act as the determining factor to
    allow webmentions. This is then used in the check for existing target.
    """
    @wraps(view, assigned=available_attrs(view))
    def inner(request, *view_args, **view_kwargs):
        view.accepts_webmentions = True
        return view(request, *view_args, **view_kwargs)
    return inner
