import json
import socket
from core.app import App
from web_http.parser import HTTPParser
from web_http.response import Response

app = App()
parser = HTTPParser()

@app.route("/")
def home(request):
    return "wazzzap"

@app.route("/search")
def search(request):
    q = request.params.get("q", "")
    page = request.params.get("page", "1")
    return json.dumps({"query": q, "page": page, "results": [f"result {i}" for i in range(1, 4)]})

@app.route("/api/users", method="POST")
def create_user(request):
    if request.body_json is None:
        return json.dumps({"error": "invalid or missing JSON body"})
    return json.dumps({"created": True, "user": request.body_json})

@app.route("/login", method="POST")
def login(request):
    if request.form_data is None:
        return json.dumps({"error": "missing form data"})
    username = request.form_data.get("username", "")
    password = request.form_data.get("password", "")
    if username == "admin" and password == "secret":
        return json.dumps({"token": "abc123"})
    return json.dumps({"error": "invalid credentials"})

server = socket.socket()
server.bind(("localhost", 8080))
server.listen()

print("listenting on port 8080")


def recv_request(client):
    buf = b""
    while b"\r\n\r\n" not in buf:
        chunk = client.recv(4096)
        if not chunk:
            return None
        buf += chunk

    header_end = buf.index(b"\r\n\r\n") + 4
    header_text = buf[:header_end].decode()
    content_length = 0
    for line in header_text.split("\r\n"):
        if line.lower().startswith("content-length:"):
            content_length = int(line.split(":", 1)[1].strip())
            break

    body = buf[header_end:]
    while len(body) < content_length:
        chunk = client.recv(4096)
        if not chunk:
            break
        body += chunk

    return buf[:header_end] + body


while True:
    client, addr = server.accept()

    raw_data = recv_request(client)
    if raw_data is None:
        client.close()
        continue

    request = parser.parse(raw_data)

    handler = app.router.resolve(
        request.method,
        request.path
    )

    if handler:
        result = handler(request)
        response = Response(result)
    else:
        response = Response(
            "404 Not Found",
            status=404
        )

    client.send(response.build())
    client.close()