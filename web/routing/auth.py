from functools import wraps
from http import HTTPStatus

from flask import request, abort

from helper_utils import is_token_valid
# from common import constants as constants
from logger import logger


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not is_token_valid(auth.token):
            logger.error('Invalid Token for Auth')
            abort(HTTPStatus.UNAUTHORIZED)
        return func(*args, **kwargs)

    return wrapper


# Custom decorator for conditional decoration
def conditional_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if auth and auth.token == 'None':
            return func(*args, **kwargs)

        if not auth or not is_token_valid(auth.token):
            logger.error('Invalid Token for Auth')
            abort(HTTPStatus.UNAUTHORIZED)
        return func(*args, **kwargs)

    return wrapper
