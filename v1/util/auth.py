import jwt

from flask import request, g
from v1.util.values import Keys, Reasons
from v1.models.essence import User
from v1.util.exceptions import ApiException
from functools import wraps


def create_access_token(user: User):
    payload = {
        Keys.USER_ID: user.u_id,
        Keys.NAME: user.name,
        Keys.EMAIL: user.email
    }
    return jwt.encode(payload=payload, key=get_secret(), algorithm="HS256").decode("utf-8")


def access_token_required(f):
    @wraps(f)
    def __wrapper(*args, **kwargs):

        headers = request.headers

        if Keys.AUTHORIZATION not in headers:
            raise ApiException(pointer=Keys.AUTHORIZATION, reason=Reasons.MISSED, code=401)

        token = headers[Keys.AUTHORIZATION]

        try:
            token_payload = jwt.decode(token, get_secret(), algorithms=["HS256"])
            g.user_id = token_payload[Keys.USER_ID]
        except:
            raise ApiException(pointer=Keys.AUTHORIZATION, reason=Reasons.INVALID, code=401)

        return f(*args, **kwargs)

    return __wrapper


def get_secret() -> str:
    return "Super secret"
