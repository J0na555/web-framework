import socket
from core.app import App
from core.middleware import run_middlewares
from web_http.parser import HTTPParser
from web_http.response import Response
from template.loader import render
from middleware.logger import logger
from middleware.auth import auth
from middleware.cors import cors

app = App()
parser = HTTPParser()

app.use(logger)
app.use(auth)
app.use(cors)

@app.route("/")
def home(request):
    return render("home.html", {"title": "Home", "body": "Welcome to the framework"})

@app.route("/users", method="GET")
def users_list(request):
    return render("users/list.html", {
        "title": "Users",
        "users": ["Alice", "Bob", "Charlie"],
        "message": request.params.get("msg", "")
    })

@app.route("/users/:id", method="GET")
def users_show(request):
    user_id = request.route_params["id"]
    return render("users/show.html", {
        "title": f"User {user_id}",
        "user_id": user_id,
        "name": f"User {user_id}",
        "email": f"user{user_id}@example.com",
        "active": True
    })

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

@app.route("/api/users")
def list_users_api(request):
    return Response.json({"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]})

@app.route("/login", method="POST")
def login(request):
    if request.form_data is None:
        return Response.json({"error": "missing form data"}, status=400)
    username = request.form_data.get("username", "")
    password = request.form_data.get("password", "")
    if username == "admin" and password == "secret":
        return Response.json({"token": "abc123"})
    return Response.json({"error": "invalid credentials"}, status=401)

@app.route("/api/users/:id")
def get_user_api(request):
    user_id = request.route_params["id"]
    return Response.json({"user_id": user_id, "name": f"User {user_id}"})

@app.route("/api/users/:id/posts/:post_id")
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

        def handler_fn(req, h=handler):
            result = h(req)
            if isinstance(result, Response):
                return result
            return Response(str(result))

        response = run_middlewares(app.middlewares, request, handler_fn)
    else:
        response = Response("404 Not Found", status=404)

    client.send(response.build())
    client.close()