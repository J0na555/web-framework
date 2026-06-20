class Response:
    def __init__(self, body="", status=200, headers=None):
        self.body = body
        self.status = status
        self.headers = headers or {}

    def build(self):
        reason = "OK" if self.status == 200 else "Not Found"
        status_line = f"HTTP/1.1 {self.status} {reason}\r\n"
        headers = ''

        body_bytes = self.body.encode() if isinstance(self.body, str) else self.body

        if "Content-Type" not in self.headers:
            if body_bytes.startswith(b"{") or body_bytes.startswith(b"["):
                self.headers["Content-Type"] = "application/json"
            else:
                self.headers["Content-Type"] = "text/html"

        self.headers["Content-Length"] = str(len(body_bytes))

        for key, value in self.headers.items():
            headers += f"{key}: {value}\r\n"

        return (status_line + headers + "\r\n").encode() + body_bytes

# convert python data into http bytes
