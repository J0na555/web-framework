import os
from template.engine import TemplateEngine
from web_http.response import Response

_engine = None


def _get_engine():
    global _engine
    if _engine is None:
        template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
        _engine = TemplateEngine(template_dir)
    return _engine


def render(template_name, context=None):
    engine = _get_engine()
    content = engine.render(template_name, context)
    return Response.html(content)
