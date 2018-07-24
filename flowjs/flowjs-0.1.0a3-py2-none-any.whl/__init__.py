name = "flowjs"

import requests
from file import ChunkedFile
from interfaces import IConfig, IRequest
from config import Config

class BadRequest(BaseException):
    pass


class NoContent(BaseException):
    pass


def save(destination, config, request):
    # type: (str, IConfig, IRequest) -> bool
    if not isinstance(config, IConfig):
        raise TypeError('Object passed to config was not of type `IConfig`')

    file = ChunkedFile(config, request)
    if request.is_get():
        if file.check_chunk():
            return True
        else:
            raise NoContent()
    else:
        if file.validate_chunk():
            file.save_chunk()
        else:
            raise BadRequest()

    if file.validate_file() and file.save(destination):
        return True
    return False
