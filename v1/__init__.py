import traceback

from flask.views import MethodView, request
from psycopg2.extras import RealDictCursor
from v1.models.essence import Error
from v1.util.exceptions import ApiException
from v1.util.response import get_response
from v1.util.values import Keys
from v1.util import get_db


class ApiView(MethodView):

    def __init__(self):
        self.db = get_db()
        self.cursor = self.db.cursor(cursor_factory=RealDictCursor)

    def dispatch_request(self, *args, **kwargs):
        try:
            global response

            if request.method == 'GET':
                response = self.get(*args, **kwargs)
            if request.method == 'POST':
                response = self.post(*args, **kwargs)
            if request.method == 'PUT':
                response = self.put(*args, **kwargs)
            if request.method == 'PATCH':
                response = self.patch(*args, **kwargs)
            if request.method == 'DELETE':
                response = self.delete(*args, **kwargs)

            return response

        except ApiException as e:
            error = Error(e.pointer, e.reason)
            traceback.print_exc()

            return get_response(error, True, e.code)
        except Exception as e:
            error = Error(Keys.API, str(e.args))
            traceback.print_exc()

            return get_response(error, True, 500)
