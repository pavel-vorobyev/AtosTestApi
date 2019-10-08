from flask import jsonify

from v1.models import Model
from v1.models.response import Response, ListResponse, ErrorResponse


def get_response(data: Model, is_error=False, code=200):
    if is_error:
        return jsonify(ErrorResponse(data).to_json()), code
    else:
        return jsonify(Response(data).to_json()), code


def get_list_response(data: [Model], code=200):
    return jsonify(ListResponse(data).to_json()), code
