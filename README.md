# Simple Webmention app for Django

*This is a work in progress, not ready for production use.* 

*Install at your own risk.*

This intends to be a simple and decoupled app for sending and receiving 
[Webmentions](http://indiewebcamp.com/Webmention), meaning that you can notify a 
site when content elsewhere mentions other content by URL.

## Quick start

1. Install `django-simplementions`, probably via pip: `pip install -e git+https://github.com/emilbjorklund/django-simplewebmentions.git#egg=django-simplewebmentions`
2. Add `simplementions` (and optionally, Celery – see below) to your `INSTALLED_APPS` setting:
       ```
       INSTALLED_APPS = (
            ...
            'simplewebmentions',
       )
       ```
3. Add the `simplementions` URL conf to your main `urls.py`:

       ```
       url(r'^mentions/', include('simplewebmentions.urls')),
       ```
   
   ...where the `mentions` part is up to you, of course.
4. Run `python manage.py migrate` to create the model.
5. Start the development server and visit http://127.0.0.1:8000/mentions/
   to see if you get the greeting-page.
6. (Optional:) In your models (or whereever), do 
   `from simplewebmentions.send import WebmentionSend`, and use a method somewhere
   on your model to send Webmentions at some point in your model's lifecycle.
   Example implementation (note: the `get_full_url` thing and field names are
   hypothetical:

       ```
       class MyModel(models.Model):
           ...

           def send_webmentions(self):
               """
               Send webmention to reply-to-URL.
               """
               if self.in_reply_to:
                   mention = WebmentionSend(self.get_full_url(), self.in_reply_to)
                   mention.send()
       ```

## Goals

- To be asynchronous by default (to lessen the risk of [DDOS-attacks by Webmention.](http://indiewebcamp.com/DDOS)
- To offer synchronous handling as an option.
- To have a simple yet rich model of received mentions.
- To offer simple integration with existing models to send webmentions.
- Maybe optionally check received mentions agains [Akismet](http://akismet.com/), 
  like [django-contrib-comments](https://github.com/django/django-contrib-comments) does?

## Requirements 

- [Django](https://djangoproject.com/) 1.7 (so far).
- Python 2.7 (since that's what I have on my machine and test on, so far.
- The python [webmention-tools](https://github.com/vrypan/webmention-tools) package, by Panayotis Vryonis.

## Optional dependencies:

- [Celery](http://celery.readthedocs.org/en/latest/index.html) (by default, for async tasks)
