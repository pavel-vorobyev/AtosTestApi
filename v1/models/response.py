from v1.models import JsonableModel, Model


class Response(JsonableModel):

    def __init__(self, data: Model):
        self.data = data


class ErrorResponse(JsonableModel):

    def __init__(self, error):
        self.error = error


class ListResponse(JsonableModel):

    def __init__(self, data: [Model]):
        self.data = data
