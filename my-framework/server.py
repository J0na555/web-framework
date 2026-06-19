import socket
from core.app import App
from web_http.parser import HTTPParser
from web_http.response import Response

app = App()
parser = HTTPParser()

@app.route("/")
def home(request):
    return "wazzzap"

server = socket.socket()
server.bind(("localhost", 8080))
server.listen()

print("listenting on port 8080")


while True:
    client, addr = server.accept()

    raw_data = client.recv(1024)

    request = parser.parse(raw_data)

    handler = app.router.resolve(
        request.method,
        request.path
    )

    if handler:
        result = handler(request)
        response = Response(result)
    else:
        response = Response(
            "404 Not Found",
            status=404
        )

    client.send(response.build())
    client.close()