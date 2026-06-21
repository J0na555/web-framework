import socket
from core.app import App
from web_http.parser import HTTPParser
from web_http.response import Response

app = App()
parser = HTTPParser()

@app.route("/")
def home(request):
    return Response.html("<h1>wazzzap</h1>")

@app.route("/search")
def search(request):
    q = request.params.get("q", "")
    page = request.params.get("page", "1")
    return Response.json({"query": q, "page": page, "results": [f"result {i}" for i in range(1, 4)]})

@app.route("/api/users", method="POST")
def create_user(request):
    if request.body_json is None:
        return Response.json({"error": "invalid or missing JSON body"}, status=400)
    return Response.json({"created": True, "user": request.body_json}, status=201)

@app.route("/login", method="POST")
def login(request):
    if request.form_data is None:
        return Response.json({"error": "missing form data"}, status=400)
    username = request.form_data.get("username", "")
    password = request.form_data.get("password", "")
    if username == "admin" and password == "secret":
        return Response.json({"token": "abc123"})
    return Response.json({"error": "invalid credentials"}, status=401)

@app.route("/users/:id")
def get_user(request):
    user_id = request.route_params["id"]
    return Response.json({"user_id": user_id, "name": f"User {user_id}"})

@app.route("/users/:id/posts/:post_id")
def get_user_post(request):
    user_id = request.route_params["id"]
    post_id = request.route_params["post_id"]
    return Response.json({"user_id": user_id, "post_id": post_id})

@app.route("/static/*")
def serve_static(request):
    filepath = request.route_params["*"]
    return Response.json({"file": filepath})

@app.route("/old-page")
def old_page(request):
    return Response.redirect("/")

@app.route("/gone")
def gone(request):
    return Response.json({"error": "resource removed"}, status=410)

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

    handler, route_params = app.router.resolve(
        request.method,
        request.path
    )

    if handler:
        request.route_params = route_params
        result = handler(request)
        if isinstance(result, Response):
            response = result
        else:
            response = Response(str(result))
    else:
        response = Response("404 Not Found", status=404)

    client.send(response.build())
    client.close()