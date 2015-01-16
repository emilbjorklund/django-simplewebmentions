from __future__ import unicode_literals
from urlparse import urlparse

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import get_current_site
from django.utils.encoding import python_2_unicode_compatible


# DRY config for webmention status
MENTION_STATUS_PUBLIC = 'public'
MENTION_STATUS_UNMODERATED = 'unmoderated'
MENTION_STATUS_DELETED = 'deleted'
MENTION_STATUSES = (
    (MENTION_STATUS_PUBLIC, _('public')),
    (MENTION_STATUS_UNMODERATED, _('unmoderated')),
    (MENTION_STATUS_DELETED, _('deleted'))
    )

class WebMentionManager(models.Manager):

    def published(self):
        return super(
            WebMentionManager, self).get_queryset().filter(status=MENTION_STATUS_PUBLIC)

class WebMention(models.Model):
    """
    A model class for handling WebMentions in a generic way.
    """
    # Where the mention comes from
    source = models.URLField(_('source url'))
    # Source title, if existing:
    source_title = models.CharField(_('source title'), max_length=255, blank=True)
    # When was the mention published?
    source_pub_date = models.DateTimeField(_('source publication date'), blank=True, null=True)
    # Which URL on your site the mention points to
    target = models.URLField(_('target URL'))
    # Does it have an "In reply to"-field?
    in_reply_to = models.URLField(_('in-reply-to URL'), blank=True)
    # Potentially store the app to which the target belongs.
    target_app = models.CharField(_('target app'), max_length=64, blank=True)
    # Source text - the comment, post, quote etc:
    source_text = models.TextField(_('source text'), blank=True)
    # Source link excerpt - the piece of text where the source links to target.
    source_link_excerpt = models.TextField(_('source link excerpt'), blank=True)
    # Who wrote the mention?
    author = models.CharField(_('author'), max_length=127, blank=True)
    # Is there an author image URL?
    author_img_url = models.URLField(_('author image URL'), blank=True)
    # Status - is the mention published or...?
    status = models.CharField(
            _('status'),
            max_length=16,
            default=MENTION_STATUS_UNMODERATED,
            choices=MENTION_STATUSES)
    objects = WebMentionManager()

    def __unicode__(self):
        return self.source_title or self.source

    def get_absolute_url(self):
        return reverse('webmention_detail', args=[self.pk])

    def get_full_url(self):
        request = None
        return ''.join([
            '//',
            get_current_site(request).domain,
            self.get_absolute_url()
            ])

    def _do_is_public(self):
        """
        Utility to check for public, exposed as property.
        """
        return self.status in [MENTION_STATUS_PUBLIC]
    is_public = property(_do_is_public)

    def _do_target_path(self):
        return urlparse(self.target_url).path
    target_path = property(_do_target_path)
