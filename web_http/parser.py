import json
from urllib.parse import unquote_plus

from web_http.request import Request


class HTTPParser:
    def parse(self, raw_data):
        header_section, _, body = raw_data.partition(b"\r\n\r\n")
        text = header_section.decode()
        lines = text.split("\r\n")

        request_line = lines[0]
        method, raw_path, version = request_line.split()

        path, params = self._parse_query_string(raw_path)

        headers = {}
        for line in lines[1:]:
            if line == "":
                break
            key, value = line.split(": ", 1)
            headers[key] = value

        request = Request(method, path, version, headers, body)
        request.params = params

        self._parse_body(request)

        return request

    def _parse_query_string(self, raw_path):
        path, _, query_string = raw_path.partition("?")
        if not query_string:
            return path, {}

        params = {}
        for pair in query_string.split("&"):
            if not pair:
                continue
            key, _, value = pair.partition("=")
            params[unquote_plus(key)] = unquote_plus(value)
        return path, params

    def _parse_body(self, request):
        if not request.body:
            return

        content_type = request.headers.get("Content-Type", "")

        if content_type == "application/json":
            try:
                request.body_json = json.loads(request.body)
            except json.JSONDecodeError:
                request.body_json = None

        elif content_type == "application/x-www-form-urlencoded":
            request.form_data = self._parse_form_data(request.body)

    def _parse_form_data(self, body):
        text = body.decode()
        data = {}
        for pair in text.split("&"):
            if not pair:
                continue
            key, _, value = pair.partition("=")
            data[unquote_plus(key)] = unquote_plus(value)
        return data


# this handles the parsing of raw HTTP data into a structured Request object
