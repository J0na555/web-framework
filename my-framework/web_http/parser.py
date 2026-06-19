from web_http.request import Request


class HTTPParser:
    def parse(self, raw_data):
        text = raw_data.decode()
        lines = text.split("\r\n")

        request_line = lines[0]
        method, path, version = request_line.split()

        headers = {}

        for line in lines[1:]:
            if line == "":
                break

            key, value = line.split(": ", 1)
            headers[key] = value

        return Request(method, path, version, headers)


# this handles the parsing of raw HTTP data into a structured Request object
