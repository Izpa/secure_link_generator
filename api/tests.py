import unittest

from run import app


class IndexTestCase(unittest.TestCase):
    def setUp(self):
        self.test_client = app.test_client(self)

    def test_with_all_correct_params(self):
        response = self.test_client.get(
            '/?t=1516741096&u=aHR0cHM6Ly93d3cuYmFzZTY0ZW5jb2RlLm9yZy8=&ip=127.0.0.1&p=password',
            content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_t_param_is_required(self):
        response = self.test_client.get(
            '/?u=aHR0cHM6Ly93d3cuYmFzZTY0ZW5jb2RlLm9yZy8=&ip=127.0.0.1&p=password',
            content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_t_param_must_be_timestamp(self):
        response = self.test_client.get(
            '/?t=qwerty&u=aHR0cHM6Ly93d3cuYmFzZTY0ZW5jb2RlLm9yZy8=&ip=127.0.0.1&p=password',
            content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_u_param_is_required(self):
        response = self.test_client.get(
            '/?t=1516741096&ip=127.0.0.1&p=password',
            content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_ip_param_is_required(self):
        response = self.test_client.get(
            '/?t=1516741096&u=aHR0cHM6Ly93d3cuYmFzZTY0ZW5jb2RlLm9yZy8=&p=password',
            content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_ip_param_must_be_ip_v4(self):
        response = self.test_client.get(
            '/?t=1516741096&u=aHR0cHM6Ly93d3cuYmFzZTY0ZW5jb2RlLm9yZy8=&ip=1270.0.1&p=password',
            content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_p_param_is_required(self):
        response = self.test_client.get(
            '/?t=1516741096&u=aHR0cHM6Ly93d3cuYmFzZTY0ZW5jb2RlLm9yZy8=&ip=127.0.0.1',
            content_type='html/text')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
