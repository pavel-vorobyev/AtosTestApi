

class ApiException(Exception):

    def __init__(self, pointer, reason, code: int):
        self.pointer = pointer
        self.reason = reason
        self.code = code
