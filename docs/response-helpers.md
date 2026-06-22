# Response Helpers Update

added methods/functions

- `Response.json()` serializes data to JSON and sets `Content-Type: application/json`.
- `Response.html()` sets `Content-Type: text/html` for raw HTML responses.
- `Response.redirect()` sets the `Location` header with a 302 status by default.
- `REASONS` dict maps status codes to proper HTTP reason phrases (201 Created, 401 Unauthorized, etc.).

this helps

- removes manual `json.dumps()` and header setting from handlers
- makes response intent explicit (`.json()` vs `.html()` vs `.redirect()`)
- consistent status codes across the framework

## Testing with curl

Start the server:

```bash
cd my-framework && python server.py
```

### JSON response

```bash
curl http://localhost:8080/search?q=hello&page=2
```

### JSON with status code

```bash
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "jonas", "age": 30}'
```

### JSON error responses

```bash
curl -X POST http://localhost:8080/api/users
curl -X POST http://localhost:8080/login -d "username=wrong&password=wrong"
```

### Redirect

```bash
curl -v http://localhost:8080/old-page
```

### Custom status (410 Gone)

```bash
curl -v http://localhost:8080/gone
```

### HTML response

```bash
curl http://localhost:8080/
```
