import json


class Response:
    REASONS = {
        200: "OK",
        201: "Created",
        204: "No Content",
        301: "Moved Permanently",
        302: "Found",
        304: "Not Modified",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        500: "Internal Server Error",
    }

    def __init__(self, body="", status=200, headers=None):
        self.body = body
        self.status = status
        self.headers = headers or {}

    @classmethod
    def json(cls, data, status=200, headers=None):
        body = json.dumps(data)
        resp = cls(body, status, headers)
        resp.headers["Content-Type"] = "application/json"
        return resp

    @classmethod
    def html(cls, body, status=200, headers=None):
        resp = cls(body, status, headers)
        resp.headers["Content-Type"] = "text/html"
        return resp

    @classmethod
    def redirect(cls, url, status=302, headers=None):
        resp = cls("", status, headers)
        resp.headers["Location"] = url
        return resp

    def build(self):
        reason = self.REASONS.get(self.status, "Unknown")
        status_line = f"HTTP/1.1 {self.status} {reason}\r\n"
        headers = ''

        body_bytes = self.body.encode() if isinstance(self.body, str) else self.body

        if "Content-Type" not in self.headers:
            self.headers["Content-Type"] = "text/html"

        self.headers["Content-Length"] = str(len(body_bytes))

        for key, value in self.headers.items():
            headers += f"{key}: {value}\r\n"

        return (status_line + headers + "\r\n").encode() + body_bytes

# convert python data into http bytes
