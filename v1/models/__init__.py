import json


class Model:

    def __init__(self):
        pass


class JsonableModel:

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, sort_keys=False))
