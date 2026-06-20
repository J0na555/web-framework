class Request:
    def __init__(self, method, path, version, headers=None, body=None):
        self.method = method
        self.path = path
        self.version = version
        self.headers = headers if headers is not None else {}
        self.body = body or b''
        self.params = {}
        self.body_json = None
        self.form_data = None

# store the request data
