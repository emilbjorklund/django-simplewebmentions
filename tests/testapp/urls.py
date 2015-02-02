from django.conf.urls import patterns, include, url

from django.views.generic import DetailView
from simplewebmentions.helpers import accept_webmentions
from .models import BlogPost
from .views import dummy_webmention

urlpatterns = patterns('',
    url(r'^mention/', include('simplewebmentions.urls')),
    # an undecorated URL, relies on field + Registry.
    url(r'^blog/(?P<pk>\d+)/$',
        DetailView.as_view(model=BlogPost),
        name='blog_detail'),
    # Decorated URL.
    url(r'^acceptingblog/(?P<pk>)\d+/$',
        accept_webmentions(DetailView.as_view(model=BlogPost)),
        name='blog_detail'),
    url(r'^dummy/$', accept_webmentions(dummy_webmention), name='dummy'),
)