from router.router import Router

class App:
    def __init__(self):
        self.router = Router()
        self.middlewares = []

    def use(self, middleware):
        self.middlewares.append(middleware)

    def route(self, path, method="GET"):
        def decorator(handler):
            self.router.add_route(method, path, handler)
            return handler
        return decorator