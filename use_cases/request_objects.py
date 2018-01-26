import re
from datetime import datetime

from shared.request_object import ValidRequestObject, InvalidRequestObject


class GenerateSecureLinkRequestObject(ValidRequestObject):
    url_pattern = re.compile("^((?:http|ftp)s?://)?[\w.-]?(?:.[\w.-]+)+[\w\-._:/?#[\]@!$&'()*+,;=]+$")
    ip_address_pattern = re.compile('^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$')

    def __new__(cls, expires: int=None, url: str=None, ip_address: str=None, password: str=None):
        invalid_request = InvalidRequestObject()
        instance = super().__new__(cls)

        if not (isinstance(expires, int) and expires >= 0):
            invalid_request.add_error('expires', 'Is not correct timestamp (positive integer)')
        elif expires < datetime.now().timestamp():
            invalid_request.add_error('expires', 'Is expired timestamp')
        else:
            instance.expires = expires

        if not (isinstance(url, str) and cls.url_pattern.match(url)):
            invalid_request.add_error('url', 'Is not correct url or path')
        else:
            instance.url = url

        if not (isinstance(ip_address, str) and cls.ip_address_pattern.match(ip_address)):
            invalid_request.add_error('ip_address', 'Is not correct ip-address')
        else:
            instance.ip_address = ip_address

        if not isinstance(password, str):
            invalid_request.add_error('password', 'Is not string')
        else:
            instance.password = password

        if invalid_request.has_errors():
            return invalid_request

        return instance
