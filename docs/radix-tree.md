# Radix Tree Routing Update

added methods/functions

- `insert` documents how each path segment is processed.
- `search` explains the route matching order and the role of static, parameter, and wildcard segments.
- helper methods  describe their simple support tasks: splitting paths, finding static children, and finding parameter children.

this helps

- improves readability
- makes the route insertion and lookup behavior easier to follow
- keeps the framework behavior unchanged while boosting maintainability

## Testing with curl

Start the server:

```bash
cd my-framework && python server.py
```

### Static routes

```bash
curl http://localhost:8080/
```

### Query params

```bash
curl "http://localhost:8080/search?q=hello&page=2"
```

### Dynamic params (`:id`)

```bash
curl http://localhost:8080/users/42
```

### Multiple dynamic params

```bash
curl http://localhost:8080/users/42/posts/7
```

### Static priority over param

`/users/profile` should match the static route, not `:id`:

```bash
curl http://localhost:8080/users/profile
```

### Wildcard (`*`)

```bash
curl http://localhost:8080/static/js/app.js
curl http://localhost:8080/static/
```

### JSON body (POST)

```bash
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "jonas", "age": 30}'
```

### Form data (POST)

```bash
curl -X POST http://localhost:8080/login \
  -d "username=admin&password=secret"
```

### 404 (no match)

```bash
curl http://localhost:8080/nonexistent
```
