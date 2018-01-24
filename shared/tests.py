from unittest import mock, main, TestCase

from shared.request_object import InvalidRequestObject, ValidRequestObject
from shared.response_object import ResponseFailure, ResponseSuccess
from shared.use_case import UseCase


class RequestObjectTestCase(TestCase):
    def test_invalid_request_object_is_false(self):
        request = InvalidRequestObject()

        self.assertFalse(bool(request))

    def test_invalid_request_object_accepts_errors(self):
        request = InvalidRequestObject()
        request.add_error(parameter='aparam', message='wrong value')
        request.add_error(parameter='anotherparam', message='wrong type')

        self.assertTrue(request.has_errors())
        self.assertEqual(len(request.errors), 2)

    def test_valid_request_object_is_true(self):
        request = ValidRequestObject()
        self.assertTrue(bool(request))


class UseCaseTestCase(TestCase):
    def test_use_case_cannot_process_valid_requests(self):
        valid_request_object = mock.MagicMock()
        valid_request_object.__bool__.return_value = True

        use_case = UseCase()
        response = use_case.execute(valid_request_object)

        self.assertFalse(response)
        self.assertEqual(response.type, ResponseFailure.SYSTEM_ERROR)
        self.assertEqual(response.message, 'NotImplementedError: process_request() not implemented by UseCase class')

    def test_use_case_can_process_invalid_requests_and_returns_response_failure(self):
        invalid_request_object = InvalidRequestObject()
        invalid_request_object.add_error('someparam', 'somemessage')

        use_case = UseCase()
        response = use_case.execute(invalid_request_object)

        self.assertFalse(response)
        self.assertEqual(response.type, ResponseFailure.PARAMETERS_ERROR)
        self.assertEqual(response.message, 'someparam: somemessage')

    def test_use_case_can_manage_generic_exception_from_process_request(self):
        use_case = UseCase()

        class TestException(Exception):
            pass

        use_case.process_request = mock.Mock()
        use_case.process_request.side_effect = TestException('somemessage')
        response = use_case.execute(mock.Mock)

        self.assertFalse(response)
        self.assertEqual(response.type, ResponseFailure.SYSTEM_ERROR)
        self.assertEqual(response.message, 'TestException: somemessage')


class ResponseObjectTestCase(TestCase):
    def setUp(self):
        self.response_value = {'key': ['value1', 'value2']}
        self.response_type = 'ResponseError'
        self.response_message = 'This is a response error'

    def test_response_success_is_true(self):
        self.assertTrue(bool(ResponseSuccess(self.response_value)))

    def test_response_failure_is_false(self):
        self.assertFalse(bool(ResponseFailure(self.response_type, self.response_message)))

    def test_response_success_contains_value(self):
        response = ResponseSuccess(self.response_value)

        self.assertEqual(response.value, self.response_value)

    def test_response_failure_has_type_and_message(self):
        response = ResponseFailure(self.response_type, self.response_message)

        self.assertEqual(response.type, self.response_type)
        self.assertEqual(response.message, self.response_message)

    def test_response_failure_contains_value(self):
        response = ResponseFailure(self.response_type, self.response_message)

        self.assertEqual(response.value, {'type': self.response_type, 'message': self.response_message})

    def test_response_failure_initialization_with_exception(self):
        response = ResponseFailure(self.response_type, Exception('Just an error message'))

        self.assertFalse(bool(response))
        self.assertEqual(response.type, self.response_type)
        self.assertEqual(response.message, "Exception: Just an error message")

    def test_response_failure_from_invalid_request_object(self):
        response = ResponseFailure.build_from_invalid_request_object(InvalidRequestObject())

        self.assertFalse(bool(response))

    def test_response_failure_from_invalid_request_object_with_errors(self):
        request_object = InvalidRequestObject()
        request_object.add_error('path', 'Is mandatory')
        request_object.add_error('path', "can't be blank")

        response = ResponseFailure.build_from_invalid_request_object(request_object)

        self.assertFalse(bool(response))
        self.assertEqual(response.type, ResponseFailure.PARAMETERS_ERROR)
        self.assertEqual(response.message, "path: Is mandatory\npath: can't be blank")

    def test_response_failure_build_resource_error(self):
        response = ResponseFailure.build_resource_error("test message")

        self.assertFalse(bool(response))
        self.assertEqual(response.type, ResponseFailure.RESOURCE_ERROR)
        self.assertEqual(response.message, "test message")

    def test_response_failure_build_parameters_error(self):
        response = ResponseFailure.build_parameters_error("test message")

        self.assertFalse(bool(response))
        self.assertEqual(response.type, ResponseFailure.PARAMETERS_ERROR)
        self.assertEqual(response.message, "test message")

    def test_response_failure_build_system_error(self):
        response = ResponseFailure.build_system_error("test message")

        self.assertFalse(bool(response))
        self.assertEqual(response.type, ResponseFailure.SYSTEM_ERROR)
        self.assertEqual(response.message, "test message")


if __name__ == '__main__':
    main()
