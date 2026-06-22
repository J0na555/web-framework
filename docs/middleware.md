# Middleware System Update

added methods/functions

- `run_middlewares()` chains middleware functions around the handler using the `next(req)` pattern.
- `app.use()` registers middleware on the App instance.
- `middleware/logger.py` logs method, path, status code, and elapsed time.
- `middleware/auth.py` blocks `/api/*` routes without an `Authorization` header.
- `middleware/cors.py` adds `Access-Control-Allow-Origin`, `Allow-Methods`, and `Allow-Headers` headers.

this helps

- separates cross-cutting concerns (logging, auth, CORS) from route handlers
- each middleware is a single function in its own file
- middleware can modify the request, modify the response, or short-circuit the chain

## How it works

Each middleware is a function that receives `(request, next)`:

```python
def my_middleware(request, next):
    # before handler
    response = next(request)
    # after handler
    return response
```

Call `next(request)` to continue the chain. Return a `Response` without calling `next` to short-circuit.

## Testing with curl

Start the server:

```bash
cd my-framework && python server.py
```

### Logger middleware

Every request prints a log line:

```bash
curl http://localhost:8080/
# -> GET / -> 200 (0.3ms)
```

### Auth middleware

Public routes work without auth:

```bash
curl http://localhost:8080/
curl http://localhost:8080/users/42
```

API routes without auth are blocked:

```bash
curl http://localhost:8080/api/users
# -> 401 missing authorization header
```

API routes with auth pass through:

```bash
curl -H "Authorization: Bearer abc123" http://localhost:8080/api/users
```

### CORS middleware

Check CORS headers on any response:

```bash
curl -v http://localhost:8080/ 2>&1 | grep -i access-control
# -> Access-Control-Allow-Origin: *
# -> Access-Control-Allow-Methods: GET, POST, PUT, DELETE, PATCH, OPTIONS
# -> Access-Control-Allow-Headers: Content-Type, Authorization
```

### All three together

```bash
curl -v -H "Authorization: Bearer abc123" http://localhost:8080/api/users 2>&1 | grep -E "(HTTP/|Access-Control|authorization)"
```