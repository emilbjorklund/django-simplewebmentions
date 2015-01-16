from __future__ import unicode_literals

from django.conf.urls import patterns,url

from simplewebmentions.views import WebMentionEndpoint, WebMentionDetail

urlpatterns = patterns('',
    url(r'(?P<pk>\d+)/$', WebMentionDetail.as_view(), name='webmention_detail'),
    url(r'^$', WebMentionEndpoint.as_view(), name='webmention_endpoint'),
    )