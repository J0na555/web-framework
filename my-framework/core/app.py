from router.router import Router

class App:
    def __init__(self):
        self.router = Router()
    
    def route(self, path, method="GET"):
        def decorator(handler):
            self.router.add_route(method, path, handler)
            return handler
        return decorator