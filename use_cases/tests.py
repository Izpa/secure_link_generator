from unittest import TestCase

from use_cases.request_objects import GenerateSecureLinkRequestObject


class BuildGenerateSecureLinkRequestObjectTestCase(TestCase):
    def setUp(self):
        self.correct_params_dict = {
            'expires': 1516741096,
            'url': 'https://qwerty.ru/',
            'ip_address': '127.0.0.1',
            'password': 'password'
        }

    def test_with_all_correct_params(self):
        request_object = GenerateSecureLinkRequestObject(**self.correct_params_dict)

        self.assertEqual(bool(request_object), True)
        for key, value in self.correct_params_dict.items():
            self.assertEqual(value, getattr(request_object, key))

    def test_expires_param_is_required(self):
        self.correct_params_dict.pop('expires')

        request_object = GenerateSecureLinkRequestObject(**self.correct_params_dict)

        self.assertTrue(request_object.has_errors())
        self.assertFalse(request_object)
        self.assertEqual(request_object.errors[0]['parameter'], 'expires')

    def test_expires_param_must_be_correct_timestamp(self):
        self.correct_params_dict['expires'] = 'qwerty'

        request_object = GenerateSecureLinkRequestObject(**self.correct_params_dict)

        self.assertTrue(request_object.has_errors())
        self.assertFalse(request_object)
        self.assertEqual(request_object.errors[0]['parameter'], 'expires')

    def test_url_param_is_required(self):
        self.correct_params_dict.pop('url')

        request_object = GenerateSecureLinkRequestObject(**self.correct_params_dict)

        self.assertTrue(request_object.has_errors())
        self.assertFalse(request_object)
        self.assertEqual(request_object.errors[0]['parameter'], 'url')

    def test_url_param_must_be_correct_url(self):
        self.correct_params_dict['url'] = 'qwerty'

        request_object = GenerateSecureLinkRequestObject(**self.correct_params_dict)

        self.assertTrue(request_object.has_errors())
        self.assertFalse(request_object)
        self.assertEqual(request_object.errors[0]['parameter'], 'url')

    def test_ip_address_param_is_required(self):
        self.correct_params_dict.pop('ip_address')

        request_object = GenerateSecureLinkRequestObject(**self.correct_params_dict)

        self.assertTrue(request_object.has_errors())
        self.assertFalse(request_object)
        self.assertEqual(request_object.errors[0]['parameter'], 'ip_address')

    def test_ip_address_param_must_be_ip_address_v4(self):
        self.correct_params_dict['ip_address'] = '1270.0.1'

        request_object = GenerateSecureLinkRequestObject(**self.correct_params_dict)

        self.assertTrue(request_object.has_errors())
        self.assertFalse(request_object)
        self.assertEqual(request_object.errors[0]['parameter'], 'ip_address')

    def test_password_param_is_required(self):
        self.correct_params_dict.pop('password')

        request_object = GenerateSecureLinkRequestObject(**self.correct_params_dict)

        self.assertTrue(request_object.has_errors())
        self.assertFalse(request_object)
        self.assertEqual(request_object.errors[0]['parameter'], 'password')
