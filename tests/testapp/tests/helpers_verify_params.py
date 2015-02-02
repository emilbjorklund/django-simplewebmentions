from django.test import TestCase
from simplewebmentions.helpers import verify_params

class TestVerifyParams(TestCase):

    def test_verify_params_both(self):
        dict = {'target': 'foo', 'source': 'bar'}
        self.assertTrue(verify_params(dict))

    def test_verify_params_source_only(self):
        dict = {'source': 'bar'}
        self.assertFalse(verify_params(dict))

    def test_verify_params_target_only(self):
        dict = {'target': 'bar'}
        self.assertFalse(verify_params(dict))

    def test_verify_params_none(self):
        dict = {}
        self.assertFalse(verify_params(dict))

    def test_verify_params_source_empty(self):
        dict = {'source': '', 'target': 'Bar'}
        self.assertFalse(verify_params(dict))

    def test_verify_params_target_empty(self):
        dict = {'source': 'Bar', 'target': ''}
        self.assertFalse(verify_params(dict))