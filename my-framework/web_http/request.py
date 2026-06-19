class Request:
    def __init__(self, method, path, version, headers=None, body=None):
        self.method = method
        self.path = path
        self.version = version
        self.headers = headers if headers is not None else {}
        self.body = body or b''
        self.params = {}

# store the request data
