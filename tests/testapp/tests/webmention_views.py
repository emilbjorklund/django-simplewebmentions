from __future__ import absolute_import

from django.test import TestCase, Client, RequestFactory
from django.core.urlresolvers import reverse
from django.utils.timezone import now

from ..models import BlogPost

class WebmentionEndpointTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.decorated = BlogPost.objects.create(
            title="Test decorator",
            slug="test-decorator",
            body="Test decorator",
            pub_date=now())

    def test_template_used(self):
        response = self.client.get(reverse('webmention_endpoint'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webmentions/webmention_endpoint.html')

    def test_head_endpoint(self):
        response = self.client.head(reverse('webmention_endpoint'))
        self.assertEqual(response.status_code, 405)

    def test_put_endpoint(self):
        response = self.client.put(reverse('webmention_endpoint'))
        self.assertEqual(response.status_code, 405)

    def test_delete_endpoint(self):
        response = self.client.delete(reverse('webmention_endpoint'))
        self.assertEqual(response.status_code, 405)

    def test_patch_endpoint(self):
        response = self.client.patch(reverse('webmention_endpoint'))
        self.assertEqual(response.status_code, 405)

    def test_link_header_exists(self):
        """
        TODO: this is not a valuable test, it should test the decorator instead.
        """
        response = self.client.get(reverse('webmention_endpoint'))
        self.assertEqual(response.Link, reverse('webmention_endpoint'))

    def test_decorator_sets_property(self):
        """
        Any view decorated with the accepts_webmentions decorator should
        have an accessible property that is accessible from inside the
        view.
        """
        response = self.client.get(reverse('dummy'))
        self.assertEqual(response.status_code, 200)
