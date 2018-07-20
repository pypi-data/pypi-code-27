"""Exception classes."""

__all__ = [

    # Base class for all HTTP exceptions.
    'HTTPException',

    # Redirect exceptions (3xx).
    'RedirectException', 'MovedPermanently', 'Found', 'SeeOther',
    'TemporaryRedirect',

    # Client exceptions (4xx).
    'BadRequest', 'Unauthorized', 'PaymentRequired', 'Forbidden', 'NotFound',
    'MethodNotAllowed', 'NotAcceptable', 'ProxyAuthenticationRequired',
    'RequestTimeout', 'Conflict', 'Gone', 'LengthRequired',
    'PreconditionFailed', 'RequestEntityTooLarge', 'RequestURITooLarge',
    'UnsupportedMediaType', 'RequestedRangeNotSatisfiable',
    'ExpectationFailed', 'UnprocessableEntity', 'Locked', 'FailedDependency',
    'UpgradeRequired', 'PreconditionRequired', 'TooManyRequests',
    'RequestHeaderFieldsTooLarge',

    # Server exceptions (5xx).
    'InternalServerError', 'NotImplemented', 'BadGateway',
    'ServiceUnavailable', 'GatewayTimeout', 'HTTPVersionNotSupported'
]


class HTTPException(Exception):
    """Base class for all HTTP exceptions."""

    code = None

    def __init__(self, phrase=None, description=None):

        if phrase is not None:
            self.phrase = phrase

        if description is not None:
            self.description = description


# Redirect exceptions (3xx).

class RedirectException(HTTPException):
    """Base class for all redirect exceptions."""
    new_url = None


class MovedPermanently(RedirectException):
    code = 301
    phrase = 'Moved Permanently'
    description = 'Object moved permanently -- see URI list'


class Found(RedirectException):
    code = 302
    phrase = 'Found'
    description = 'Object moved temporarily -- see URI list'


class SeeOther(RedirectException):
    code = 303
    phrase = 'See Other'
    description = 'Object moved -- see Method and URL list'


class TemporaryRedirect(RedirectException):
    code = 307
    phrase = 'Temporary Redirect'
    description = 'Object moved temporarily -- see URI list'


# Client exceptions (4xx).

class BadRequest(HTTPException):
    code = 400
    phrase = 'Bad Request'
    description = 'Bad request syntax or unsupported method'


class Unauthorized(HTTPException):
    code = 401
    phrase = 'Unauthorized'
    description = 'No permission -- see authorization schemes'


class PaymentRequired(HTTPException):
    code = 402
    phrase = 'Payment Required'
    description = 'No payment -- see charging schemes'


class Forbidden(HTTPException):
    code = 403
    phrase = 'Forbidden'
    description = 'Request forbidden -- authorization will not help'


class NotFound(HTTPException):
    code = 404
    phrase = 'Not Found'
    description = 'Nothing matches the given URI'


class MethodNotAllowed(HTTPException):
    code = 405
    phrase = 'Method Not Allowed'
    description = 'Specified method is invalid for this resource'


class NotAcceptable(HTTPException):
    code = 406
    phrase = 'Not Acceptable'
    description = 'URI not available in preferred format'


class ProxyAuthenticationRequired(HTTPException):
    code = 407
    phrase = 'Proxy Authentication Required'
    description = 'You must authenticate with this proxy before proceeding'


class RequestTimeout(HTTPException):
    code = 408
    phrase = 'Request Timeout'
    description = 'Request timed out; try again later'


class Conflict(HTTPException):
    code = 409
    phrase = 'Conflict'
    description = 'Request conflict'


class Gone(HTTPException):
    code = 410
    phrase = 'Gone'
    description = 'URI no longer exists and has been permanently removed'


class LengthRequired(HTTPException):
    code = 411
    phrase = 'Length Required'
    description = 'Client must specify Content-Length'


class PreconditionFailed(HTTPException):
    code = 412
    phrase = 'Precondition Failed'
    description = 'Precondition in headers is false'


class RequestEntityTooLarge(HTTPException):
    code = 413
    phrase = 'Request Entity Too Large'
    description = 'Entity is too large'


class RequestURITooLarge(HTTPException):
    code = 414
    phrase = 'Request-URI Too Long'
    description = 'URI is too long'


class UnsupportedMediaType(HTTPException):
    code = 415
    phrase = 'Unsupported Media Type'
    description = 'Entity body in unsupported format'


class RequestedRangeNotSatisfiable(HTTPException):
    code = 416
    phrase = 'Requested Range Not Satisfiable'
    description = 'Cannot satisfy request range'


class ExpectationFailed(HTTPException):
    code = 417
    phrase = 'Expectation Failed'
    description = 'Expect condition could not be satisfied'


class UnprocessableEntity(HTTPException):
    code = 422
    phrase = 'Unprocessable Entity'
    description = ''


class Locked(HTTPException):
    code = 423
    phrase = 'Locked'
    description = 'Locked'


class FailedDependency(HTTPException):
    code = 424
    phrase = 'Failed Dependency'
    description = 'Failed Dependency'


class UpgradeRequired(HTTPException):
    code = 426
    phrase = 'Upgrade Required'
    description = 'Upgrade Required'


class PreconditionRequired(HTTPException):
    code = 428
    phrase = 'Precondition Required'
    description = 'The origin server requires the request to be conditional'


class TooManyRequests(HTTPException):
    code = 429
    phrase = 'Too Many Requests'
    description = 'The user has sent too many requests in a given amount of ' \
                  'time ("rate limiting") '


class RequestHeaderFieldsTooLarge(HTTPException):
    code = 431
    phrase = 'Request Header Fields Too Large'
    description = 'The server is unwilling to process the request because ' \
                  'its header fields are too large '


# Server exceptions (5xx).

class InternalServerError(HTTPException):
    code = 500
    phrase = 'Internal Server Error'
    description = 'Server got itself in trouble'


class NotImplemented(HTTPException):
    code = 501
    phrase = 'Not Implemented'
    description = 'Server does not support this operation'


class BadGateway(HTTPException):
    code = 502
    phrase = 'Bad Gateway'
    description = 'Invalid responses from another server/proxy'


class ServiceUnavailable(HTTPException):
    code = 503
    phrase = 'Service Unavailable'
    description = 'The server cannot process the request due to a high load'


class GatewayTimeout(HTTPException):
    code = 504
    phrase = 'Gateway Timeout'
    description = 'The gateway server did not receive a timely response'


class HTTPVersionNotSupported(HTTPException):
    code = 505
    phrase = 'HTTP Version Not Supported'
    description = 'Cannot fulfill request'
