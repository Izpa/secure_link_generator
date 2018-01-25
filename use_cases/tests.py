from unittest import TestCase
from urllib.parse import urlparse, parse_qsl

from use_cases.request_objects import GenerateSecureLinkRequestObject
from use_cases.generate_secure_link_use_cases import GenerateSecureLinkUseCase


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


class GenerateSecureLinkUseCaseTestCase(TestCase):
    def setUp(self):
        self.secure_link_use_case = GenerateSecureLinkUseCase()
        self.url = 'http://stackoverflow.com/search?q=question'
        self.correct_params_dict = {
            'expires': 1516741096,
            'url': self.url,
            'ip_address': '127.0.0.1',
            'password': 'password'
        }
        self.correct_md5 = '560e6b3ade697e2fd86b657ad3ade7de'

    def test_generate_md5_to_secure_link(self):
        md5 = GenerateSecureLinkUseCase._generate_md5_to_secure_link(**self.correct_params_dict)

        self.assertEqual(md5, self.correct_md5)

    def test_add_query_to_url(self):
        query_dict = {'lang': 'en', 'tag': 'python'}

        correct_url_with_new_query = 'http://stackoverflow.com/search?q=question&lang=en&tag=python'
        parsed_correct_url_with_new_query = urlparse(correct_url_with_new_query)
        correct_url_with_new_query_query_dict = dict(parse_qsl(parsed_correct_url_with_new_query.query))

        url_with_new_query = GenerateSecureLinkUseCase._add_query_to_url(url=self.url, query_dict=query_dict)
        parsed_url_with_new_query = urlparse(url_with_new_query)
        url_with_new_query_query_dict = dict(parse_qsl(parsed_url_with_new_query.query))

        self.assertEqual(parsed_url_with_new_query.scheme, parsed_correct_url_with_new_query.scheme)
        self.assertEqual(parsed_url_with_new_query.netloc, parsed_correct_url_with_new_query.netloc)
        self.assertEqual(parsed_url_with_new_query.path, parsed_correct_url_with_new_query.path)
        self.assertEqual(parsed_url_with_new_query.params, parsed_correct_url_with_new_query.params)
        self.assertEqual(parsed_url_with_new_query.fragment, parsed_correct_url_with_new_query.fragment)
        self.assertDictEqual(correct_url_with_new_query_query_dict, url_with_new_query_query_dict)

    def test_remove_query_from_url(self):
        correct_url_without_query = 'http://stackoverflow.com/search'
        url_without_query = GenerateSecureLinkUseCase._remove_query_from_url(self.url)

        self.assertEqual(correct_url_without_query, url_without_query)

    def test_process_request_handles_bad_request(self):
        request_object = GenerateSecureLinkRequestObject()

        response_object = self.secure_link_use_case.execute(request_object)

        self.assertFalse(bool(response_object))
        self.assertEqual(response_object.value,
                         {'message': 'expires: Is not correct timestamp (positive integer)\n'
                                     'url: Is not correct url\n'
                                     'ip_address: Is not correct ip-address\n'
                                     'password: Is not string',
                          'type': 'PARAMETERS_ERROR'})

    def test_process_request_with_correct_request(self):
        correct_secure_link = 'http://stackoverflow.com/search?q=question&md5=560e6b3ade697e2fd86b657ad3ade7de'
        request_object = GenerateSecureLinkRequestObject(**self.correct_params_dict)
        response_object = self.secure_link_use_case.execute(request_object)

        self.assertTrue(bool(response_object))
        self.assertEqual(response_object.value, correct_secure_link)
