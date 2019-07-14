"""

Global Utility Classes

"""
from contextlib import contextmanager
from urllib.parse import urlencode
from urllib.parse import parse_qs, urlsplit, urlunsplit


class CustomException(Exception):
    status_code = 400
    """
    CustomException class to raise Custom API Exception with status_code
    and payload
    """

    def __init__(self, message, status_code=None, payload=None, send_email=False):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        self.send_email = send_email

    def _repr(self):
        rv = dict(self.payload or ())
        rv['error_msg'] = self.message
        rv['status'] = 'failed'
        rv['code'] = self.status_code
        return rv

    def _send_exception_email(self):
        return self.send_email

    def __str__(self):
        return self.message


class Codes:
    def __init__(self):
        pass
    Ok = OK = PASS = 200
    CREATED = 201
    ACCEPTED = 202
    RESET = 205
    SEE_OTHER = 303
    LOGIN_REQUIRED = 401
    REQUIRED_PARAMETER = 402
    ACCESS_DENIED = 403
    NOT_FOUND = 404
    NOT_ALLOWED = 405
    FAIL = 501
    INTERNAL_ERROR = 500
    TOKEN_EXPIRE = 1202
    NULL_PARAM = 1201
    INVALID_PARAM = 1203
    CONFLICT = 1204

class ErrorMessages:
    def __init__(self):
        pass
    default_msg = "Internal Error Occurred. We Broke Something, our experts will be fixing it up Soon !!"


@contextmanager
def suppress(*exceptions):
    try:
        yield
    except exceptions:
        pass


def set_query_parameter(url, param_name, param_value):
    """Given a URL, set or replace a query parameter and return the
    modified URL.

    >>> set_query_parameter('http://example.com?foo=bar&biz=baz', 'foo', 'stuff')
    'http://example.com?foo=stuff&biz=baz'

    """
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)

    if isinstance(query_params.get(param_name), list):
        query_params[param_name].append(param_value)
    else:
        query_params[param_name] = [param_value]
    new_query_string = urlencode(query_params, doseq=True)

    return urlunsplit((scheme, netloc, path, new_query_string, fragment))
