import unittest

from api import _create_request_object_from_request_args
from run import app


class IndexTestCase(unittest.TestCase):
    def setUp(self):
        self.test_client = app.test_client(self)

    def test_with_all_correct_params(self):
        response = self.test_client.get(
            '/?t=1516741096&u=aHR0cDovL3N0YWNrb3ZlcmZsb3cuY29tL3NlYXJjaD9xPXF1ZXN0aW9u=&ip=127.0.0.1&p=password',
            content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data,
                         b'http://stackoverflow.com/search?q=question&md5=560e6b3ade697e2fd86b657ad3ade7de')

    def test_t_param_is_required(self):
        response = self.test_client.get(
            '/?u=aHR0cDovL3N0YWNrb3ZlcmZsb3cuY29tL3NlYXJjaD9xPXF1ZXN0aW9u=&ip=127.0.0.1&p=password',
            content_type='html/text')
        self.assertEqual(response.status_code, 400)

    def test_t_param_must_be_timestamp(self):
        response = self.test_client.get(
            '/?t=qwerty&u=aHR0cDovL3N0YWNrb3ZlcmZsb3cuY29tL3NlYXJjaD9xPXF1ZXN0aW9u=&ip=127.0.0.1&p=password',
            content_type='html/text')
        self.assertEqual(response.status_code, 400)

    def test_u_param_is_required(self):
        response = self.test_client.get(
            '/?t=1516741096&ip=127.0.0.1&p=password',
            content_type='html/text')
        self.assertEqual(response.status_code, 400)

    def test_ip_param_is_required(self):
        response = self.test_client.get(
            '/?t=1516741096&u=aHR0cDovL3N0YWNrb3ZlcmZsb3cuY29tL3NlYXJjaD9xPXF1ZXN0aW9u=&p=password',
            content_type='html/text')
        self.assertEqual(response.status_code, 400)

    def test_ip_param_must_be_ip_v4(self):
        response = self.test_client.get(
            '/?t=1516741096&u=aHR0cDovL3N0YWNrb3ZlcmZsb3cuY29tL3NlYXJjaD9xPXF1ZXN0aW9u=&ip=1270.0.1&p=password',
            content_type='html/text')
        self.assertEqual(response.status_code, 400)

    def test_p_param_is_required(self):
        response = self.test_client.get(
            '/?t=1516741096&u=aHR0cDovL3N0YWNrb3ZlcmZsb3cuY29tL3NlYXJjaD9xPXF1ZXN0aW9u=&ip=127.0.0.1',
            content_type='html/text')
        self.assertEqual(response.status_code, 400)


class CreateRequestObjectFromRequestArgsTestCase(unittest.TestCase):
    def setUp(self):
        self.request_args = {
            't': '1516741096',
            'u': 'aHR0cDovL3N0YWNrb3ZlcmZsb3cuY29tL3NlYXJjaD9xPXF1ZXN0aW9u',
            'ip': '127.0.0.1',
            'p': 'password',
        }

    def test_with_all_correct_params(self):
        request_object = _create_request_object_from_request_args(self.request_args)
        self.assertEqual(1516741096, request_object.expires)
        self.assertEqual('http://stackoverflow.com/search?q=question', request_object.url)
        self.assertEqual('127.0.0.1', request_object.ip_address)
        self.assertEqual('password', request_object.password)


if __name__ == '__main__':
    unittest.main()
