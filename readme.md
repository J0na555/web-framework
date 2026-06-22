# My Framework

> 🚧 under construction

A lightweight Python web framework built from scratch on raw sockets. No dependencies.

## Features

- **HTTP Parser** — query params, JSON body, form-urlencoded body, URL decoding
- **Radix Tree Router** — dynamic params (`:id`), wildcards (`*`), static priority
- **Response Helpers** — `.json()`, `.html()`, `.redirect()`
- **Middleware** — function-based with `next(req)` chaining
- **Template Engine** — `{{ var }}`, `{% for %}`, `{% if %}` with caching

## Quick Start

```bash
cd my-framework
python server.py
```

Server runs on `http://localhost:8080`.

## Project Structure

```bash
my-framework/
├── server.py              # Entry point
├── core/
│   ├── app.py             # App class (route registration, middleware)
│   └── middleware.py      # Middleware chain runner
├── web_http/
│   ├── parser.py          # HTTP request parser
│   ├── request.py         # Request object
│   └── response.py        # Response helpers
├── router/
│   ├── router.py          # Router wrapper
│   └── radix_tree.py      # Radix tree implementation
├── middleware/
│   ├── logger.py          # Request logging
│   ├── auth.py            # API auth check
│   └── cors.py            # CORS headers
├── template/
│   ├── engine.py          # Template rendering engine
│   └── loader.py          # render() shortcut
├── templates/             # HTML template files
│   ├── home.html
│   ├── layout.html
│   └── users/
│       ├── list.html
│       └── show.html
└── docs/                  # Implementation docs
```

## Routes

```python
@app.route("/")
def home(request):
    return Response.html("<h1>Hello</h1>")

@app.route("/users/:id")
def get_user(request):
    user_id = request.route_params["id"]
    return Response.json({"id": user_id})

@app.route("/static/*")
def serve_static(request):
    filepath = request.route_params["*"]
    return Response.json({"file": filepath})
```

## Request Object

```python
request.method          # GET, POST, etc.
request.path            # /users/42 (query string stripped)
request.params          # {"page": "1"} from ?page=1
request.route_params    # {"id": "42"} from /users/:id
request.headers         # {"Content-Type": "application/json"}
request.body            # raw bytes
request.body_json       # parsed dict (if Content-Type: application/json)
request.form_data       # parsed dict (if Content-Type: application/x-www-form-urlencoded)
```

## Response Helpers

```python
Response.json({"ok": True})                # application/json
Response.json({"error": "bad"}, status=400) # with status code
Response.html("<h1>Hello</h1>")            # text/html
Response.redirect("/new-page")             # 302 redirect
Response.redirect("/gone", status=301)     # 301 redirect
```

## Middleware

```python
def my_middleware(request, next):
    # before handler
    print(f"{request.method} {request.path}")
    response = next(request)
    # after handler
    return response

app.use(my_middleware)
```

Built-in middleware in `middleware/`:

- `logger` — logs method, path, status, elapsed time
- `auth` — blocks `/api/*` without `Authorization` header
- `cors` — adds CORS headers

## Templates

```python
from template.loader import render

@app.route("/users")
def users_list(request):
    return render("users/list.html", {
        "title": "Users",
        "users": ["Alice", "Bob"]
    })
```

Template syntax:
```
{{ variable }}                          # variable substitution
{% for item in list %}...{% endfor %}   # loop
{% if var %}...{% endif %}              # conditional
```

## Testing with curl

```bash
# Home
curl http://localhost:8080/

# JSON API
curl http://localhost:8080/users/42
curl http://localhost:8080/search?q=hello&page=2

# POST JSON
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "jonas"}'

# POST form
curl -X POST http://localhost:8080/login \
  -d "username=admin&password=secret"

# Templates
curl http://localhost:8080/users
curl http://localhost:8080/users/42

# Auth (API routes)
curl http://localhost:8080/api/users                          # 401
curl -H "Authorization: Bearer abc123" http://localhost:8080/api/users  # 200
```
