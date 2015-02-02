from __future__ import absolute_import

from django.db import models

class BlogPost(models.Model):

    title = models.CharField(max_length=255)
    body = models.TextField()
    pub_date = models.DateField()
    slug = models.SlugField(max_length=255)
    allow_replies = models.BooleanField(default=False)

    def get_absolute_url(self):
        return 'blog/%s/' % self.pk

    def _do_accept_webmention(self):
        return self.accepts_webmentions
    accepts_webmentions = property(_do_accept_webmention)