import socket

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)

print(f"Listening on {SERVER_HOST}:{SERVER_PORT}")

while True:
    client_socket, client_addr = server_socket.accept()
    print(f"Connected by {client_addr}")

    request_data = client_socket.recv(4096).decode()
    print(f"Request:\n{request_data}")

    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Length: 23\r\n"
        "Content-Type: text/plain\r\n"
        "\r\n"
        "what's up mother fucker"
    )

    client_socket.sendall(response.encode())
    client_socket.close()