from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^mention/', include('simplewebmentions.urls')),
)