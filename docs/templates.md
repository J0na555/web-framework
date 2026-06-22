# Template Engine Update

added methods/functions

- `TemplateEngine.render()` reads a template file, replaces `{{ var }}` variables, `{% for %}` loops, and `{% if %}` conditionals.
- `TemplateEngine._render_variables()` handles `{{ key }}` substitution from context dict.
- `TemplateEngine._render_loops()` handles `{% for item in list %}...{% endfor %}` iteration.
- `TemplateEngine._render_conditionals()` handles `{% if var %}...{% endif %}` rendering.
- `render()` in `template/loader.py` is a shortcut that renders a template and returns a `Response.html()`.

this helps

- separates HTML from Python logic
- templates are cached after first read
- loops and conditionals work with plain context dicts

## Template syntax

```bash
{{ variable }}                      -> replaced with context[key]
{% for x in list %}...{% endfor %}  -> iterates over context[list]
{% if var %}...{% endif %}          -> renders block if context[var] is truthy
```

## Folder structure

```bash
templates/
├── home.html
├── layout.html
└── users/
    ├── list.html
    └── show.html
```

## Testing with curl

Start the server:

```bash
cd my-framework && python server.py
```

### Home page (variables)

```bash
curl http://localhost:8080/
```

### Users list (loop)

```bash
curl http://localhost:8080/users
```

### Users list with message (conditional)

```bash
curl "http://localhost:8080/users?msg=hello+world"
```

### Single user (variables + conditional)

```bash
curl http://localhost:8080/users/42
curl http://localhost:8080/users/99
```
