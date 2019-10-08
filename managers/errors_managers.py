from werkzeug.exceptions import HTTPException
from v1.util.response import get_response
from v1.models.essence import Error
from v1.util.values import Keys


def handle_error(e: HTTPException):
    error = Error(pointer=Keys.API, reason=e.description)
    return get_response(error, True, e.code)
