import re
import os


class TemplateEngine:
    def __init__(self, template_dir="templates"):
        self.template_dir = template_dir
        self.cache = {}

    def render(self, template_name, context=None):
        context = context or {}

        if template_name not in self.cache:
            path = os.path.join(self.template_dir, template_name)
            with open(path, "r") as f:
                self.cache[template_name] = f.read()

        content = self.cache[template_name]
        content = self._render_loops(content, context)
        content = self._render_conditionals(content, context)
        content = self._render_variables(content, context)

        return content

    def _render_variables(self, content, context):
        def replace_var(match):
            key = match.group(1).strip()
            return str(context.get(key, ""))

        return re.sub(r"\{\{(.*?)\}\}", replace_var, content)

    def _render_loops(self, content, context):
        loop_pattern = r"\{% for (\w+) in (\w+) %\}(.*?)\{% endfor %\}"

        def replace_loop(match):
            item_name = match.group(1)
            list_name = match.group(2)
            body = match.group(3)

            result = ""
            for item in context.get(list_name, []):
                result += re.sub(
                    r"\{\{\s*" + item_name + r"\s*\}\}",
                    str(item),
                    body,
                )
            return result

        return re.sub(loop_pattern, replace_loop, content, flags=re.DOTALL)

    def _render_conditionals(self, content, context):
        if_pattern = r"\{% if (\w+) %\}(.*?)\{% endif %\}"

        def replace_if(match):
            var_name = match.group(1)
            body = match.group(2)
            if context.get(var_name):
                return body
            return ""

        return re.sub(if_pattern, replace_if, content, flags=re.DOTALL)
