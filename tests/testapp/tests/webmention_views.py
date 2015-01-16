from django.test import TestCase, Client
from django.core.urlresolvers import reverse

class WebmentionEndpointTestCase(TestCase):

    def setUp(self):
        self.client = Client()

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
