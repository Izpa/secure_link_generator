import re

from shared.request_object import ValidRequestObject, InvalidRequestObject


class GenerateSecureLinkRequestObject(ValidRequestObject):
    url_pattern = re.compile("^((?:http|ftp)s?://)?[\w.-]?(?:.[\w\.-]+)+[\w\-._:/?#[\]@!$&'()*+,;=]+$")
    ip_address_pattern = re.compile('^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$')

    def __new__(cls, expires: int=None, url: str=None, ip_address: str=None, password: str=None):
        invalid_request = InvalidRequestObject()
        instance = super().__new__(cls)

        if isinstance(expires, int) and expires >= 0:
            instance.expires = expires
        else:
            invalid_request.add_error('expires', 'Is not correct timestamp (positive integer)')

        if isinstance(url, str) and cls.url_pattern.match(url):
            instance.url = url
        else:
            invalid_request.add_error('url', 'Is not correct url')

        if isinstance(ip_address, str) and cls.ip_address_pattern.match(ip_address):
            instance.ip_address = ip_address
        else:
            invalid_request.add_error('ip_address', 'Is not correct ip-address')

        if isinstance(password, str):
            instance.password = password
        else:
            invalid_request.add_error('password', 'Is not string')

        if invalid_request.has_errors():
            return invalid_request

        return instance
