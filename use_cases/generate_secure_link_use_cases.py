import base64
import hashlib
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

from shared.response_object import ResponseSuccess
from shared.use_case import UseCase


class GenerateSecureLinkUseCase(UseCase):
    def process_request(self, request_object):
        md5 = self._generate_hash_for_secure_link(expires=request_object.expires,
                                                  url=request_object.url,
                                                  ip_address=request_object.ip_address,
                                                  password=request_object.password)
        new_query_dict = {'md5': md5, 'expires': request_object.expires}
        secure_url = self._add_query_to_url(url=request_object.url, query_dict=new_query_dict)
        return ResponseSuccess(secure_url)

    @classmethod
    def _generate_hash_for_secure_link(cls, expires: int, url: str, ip_address: str, password: str):
        string_for_md5 = ''.join([str(expires), str(url), str(ip_address), '=', str(password)])
        md5 = hashlib.md5(string_for_md5.encode('utf-8'))
        hash_string = base64.b64encode(md5.digest()).decode()
        hash_string = hash_string.replace('+', '-')
        hash_string = hash_string.replace('/', '_')
        hash_string = hash_string.replace('=', '')

        return hash_string

    @classmethod
    def _add_query_to_url(cls, url: str, query_dict: dict):
        url_parts = list(urlparse(url))
        exist_query_dict = dict(parse_qsl(url_parts[4]))
        exist_query_dict.update(query_dict)
        url_parts[4] = urlencode(exist_query_dict)
        new_url = urlunparse(url_parts)

        return new_url

    @classmethod
    def _get_path_from_url(cls, url: str):
        return urlparse(url).path
