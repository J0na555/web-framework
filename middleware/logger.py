import time


def logger(request, next):
    start = time.time()
    response = next(request)
    elapsed = (time.time() - start) * 1000
    print(f"{request.method} {request.path} -> {response.status} ({elapsed:.1f}ms)")
    return response
