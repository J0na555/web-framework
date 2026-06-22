from web_http.response import Response


def auth(request, next):
    if request.path.startswith("/api/"):
        token = request.headers.get("Authorization")
        if not token:
            return Response.json({"error": "missing authorization header"}, status=401)
    return next(request)
