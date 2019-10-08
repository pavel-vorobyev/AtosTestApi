from flask import request
from v1 import ApiView
from v1.util.values import Keys, Reasons
from v1.provider.user import get_user, put_user, if_user_exists
from v1.models.essence import Auth, User as UserModel
from v1.util.checker import check_for_params
from v1.util.exceptions import ApiException
from v1.util.auth import create_access_token
from v1.util.response import get_response


class User(ApiView):

    def post(self):
        body = request.json
        missed_param = check_for_params([Keys.EMAIL, Keys.PASSWORD], body)

        if missed_param is not None:
            raise ApiException(pointer=missed_param, reason=Reasons.MISSED, code=400)

        email = body[Keys.EMAIL]
        password = body[Keys.PASSWORD]

        user = get_user(self.cursor, email, password)

        if user is None:
            raise ApiException(pointer=Keys.DATA, reason=Reasons.WRONG, code=400)

        token = create_access_token(user)
        data = Auth(token, user)

        return get_response(data)

    def put(self):
        body = request.json
        missed_param = check_for_params([Keys.NAME, Keys.EMAIL, Keys.PASSWORD], body)

        if missed_param is not None:
            raise ApiException(pointer=missed_param, reason=Reasons.MISSED, code=400)

        email = body[Keys.EMAIL]

        if if_user_exists(self.cursor, email):
            raise ApiException(pointer=Keys.EMAIL, reason=Reasons.TAKEN, code=409)

        name = body[Keys.NAME]
        password = body[Keys.PASSWORD]

        put_user(self.cursor, name, email, password)
        user = UserModel(None, name, email)

        return get_response(user)

